/*-------------------------------------------------------------------------
 *
 * mcxt.c
 *       POSTGRES memory context management code.
 *
 * This module handles context management operations that are independent
 * of the particular kind of context being operated on.  It calls
 * context-type-specific operations via the function pointers in a
 * context's MemoryContextMethods struct.
 *
 *
 * Portions Copyright (c) 1996-2001, PostgreSQL Global Development Group
 * Portions Copyright (c) 1994, Regents of the University of California
 *
 *
 * IDENTIFICATION
 *       $Header: /cvsroot/pgsql/src/backend/utils/mmgr/mcxt.c,v 1.29 2001/10/25 05:49:51 momjian Exp $
 *
 *-------------------------------------------------------------------------
 */
#include "postgres.h"
#include "nodes/memnodes.h"
#include "utils/excid.h"
#include "utils/memutils.h"
/*****************************************************************************
 *       GLOBAL MEMORY                                                                   *
 *****************************************************************************/
/*
 * CurrentMemoryContext
 *         Default memory context for allocations.
 */
MemoryContext CurrentMemoryContext = NULL;
/*
 * Standard top-level contexts
 */
MemoryContext TopMemoryContext = NULL;
MemoryContext ErrorContext = NULL;
MemoryContext PostmasterContext = NULL;
MemoryContext CacheMemoryContext = NULL;
MemoryContext QueryContext = NULL;
MemoryContext TopTransactionContext = NULL;
MemoryContext TransactionCommandContext = NULL;
/*****************************************************************************
 *       EXPORTED ROUTINES                                                                    *
 *****************************************************************************/
/*
 * MemoryContextInit
 *         Start up the memory-context subsystem.
 *
 * This must be called before creating contexts or allocating memory in
 * contexts.  TopMemoryContext and ErrorContext are initialized here;
 * other contexts must be created afterwards.
 *
 * In normal multi-backend operation, this is called once during
 * postmaster startup, and not at all by individual backend startup
 * (since the backends inherit an already-initialized context subsystem
 * by virtue of being forked off the postmaster).
 *
 * In a standalone backend this must be called during backend startup.
 */
void
MemoryContextInit(void) {
       AssertState(TopMemoryContext == NULL);
       /*
        * Initialize TopMemoryContext as an AllocSetContext with slow growth
        * rate --- we don't really expect much to be allocated in it.
        *
        * (There is special-case code in MemoryContextCreate() for this call.)
        */
       TopMemoryContext = AllocSetContextCreate((MemoryContext) NULL,
                                                       "TopMemoryContext",
                                                       8 * 1024,
                                                       8 * 1024,
                                                       8 * 1024);
       /*
        * Not having any other place to point CurrentMemoryContext, make it
        * point to TopMemoryContext.  Caller should change this soon!
        */
       CurrentMemoryContext = TopMemoryContext;
       /*
        * Initialize ErrorContext as an AllocSetContext with slow growth rate
        * --- we don't really expect much to be allocated in it. More to the
        * point, require it to contain at least 8K at all times. This is the
        * only case where retained memory in a context is *essential* --- we
        * want to be sure ErrorContext still has some memory even if we've
        * run out elsewhere!
        */
       ErrorContext = AllocSetContextCreate(TopMemoryContext,
                                                  "ErrorContext",
                                                  8 * 1024,
                                                  8 * 1024,
                                                  8 * 1024); }
/*
 * MemoryContextReset
 *         Release all space allocated within a context and its descendants,
 *         but don't delete the contexts themselves.
 *
 * The type-specific reset routine handles the context itself, but we
 * have to do the recursion for the children.
 */
void
MemoryContextReset(MemoryContext context) {
       AssertArg(MemoryContextIsValid(context));
       MemoryContextResetChildren(context);
       (*context->methods->reset) (context); }
/*
 * MemoryContextResetChildren
 *         Release all space allocated within a context's descendants,
 *         but don't delete the contexts themselves.  The named context
 *         itself is not touched.
 */
void
MemoryContextResetChildren(MemoryContext context) {
       MemoryContext child;
       AssertArg(MemoryContextIsValid(context));
       for (child = context->firstchild; child != NULL; child = child->nextchild)
             MemoryContextReset(child); }
/*
 * MemoryContextDelete
 *         Delete a context and its descendants, and release all space
 *         allocated therein.
 *
 * The type-specific delete routine removes all subsidiary storage
 * for the context, but we have to delete the context node itself,
 * as well as recurse to get the children.     We must also delink the
 * node from its parent, if it has one.
 */
void
MemoryContextDelete(MemoryContext context) {
       AssertArg(MemoryContextIsValid(context));
       /* We had better not be deleting TopMemoryContext ... */
       Assert(context != TopMemoryContext);
       /* And not CurrentMemoryContext, either */
       Assert(context != CurrentMemoryContext);
       MemoryContextDeleteChildren(context);
       /*
        * We delink the context from its parent before deleting it, so that
        * if there's an error we won't have deleted/busted contexts still
        * attached to the context tree.  Better a leak than a crash.
        */
       if (context->parent) {
             MemoryContext parent = context->parent;
             if (context == parent->firstchild)
                  parent->firstchild = context->nextchild;
             else {
                  MemoryContext child;
                  for (child = parent->firstchild; child; child = child->nextchild) {
                      if (context == child->nextchild) {
                         child->nextchild = context->nextchild;
                         break; } } } }
       (*context->methods->delete) (context);
       pfree(context); }
/*
 * MemoryContextDeleteChildren
 *         Delete all the descendants of the named context and release all
 *         space allocated therein.  The named context itself is not touched.
 */
void
MemoryContextDeleteChildren(MemoryContext context) {
       AssertArg(MemoryContextIsValid(context));
       /*
        * MemoryContextDelete will delink the child from me, so just iterate
        * as long as there is a child.
        */
       while (context->firstchild != NULL)
             MemoryContextDelete(context->firstchild); }
/*
 * MemoryContextResetAndDeleteChildren
 *         Release all space allocated within a context and delete all
 *         its descendants.
 *
 * This is a common combination case where we want to preserve the
 * specific context but get rid of absolutely everything under it.
 */
void
MemoryContextResetAndDeleteChildren(MemoryContext context) {
       AssertArg(MemoryContextIsValid(context));
       MemoryContextDeleteChildren(context);
       (*context->methods->reset) (context); }
/*
 * MemoryContextStats
 *         Print statistics about the named context and all its descendants.
 *
 * This is just a debugging utility, so it's not fancy.  The statistics
 * are merely sent to stderr.
 */
void
MemoryContextStats(MemoryContext context) {
       MemoryContext child;
       AssertArg(MemoryContextIsValid(context));
       (*context->methods->stats) (context);
       for (child = context->firstchild; child != NULL; child = child->nextchild)
             MemoryContextStats(child); }
/*
 * MemoryContextCheck
 *         Check all chunks in the named context.
 *
 * This is just a debugging utility, so it's not fancy.
 */
#ifdef MEMORY_CONTEXT_CHECKING
void
MemoryContextCheck(MemoryContext context) {
       MemoryContext child;
       AssertArg(MemoryContextIsValid(context));
       (*context->methods->check) (context);
       for (child = context->firstchild; child != NULL; child = child->nextchild)
             MemoryContextCheck(child); }
#endif
/*
 * MemoryContextContains
 *         Detect whether an allocated chunk of memory belongs to a given
 *         context or not.
 *
 * Caution: this test is reliable as long as 'pointer' does point to
 * a chunk of memory allocated from *some* context.  If 'pointer' points
 * at memory obtained in some other way, there is a small chance of a
 * false-positive result, since the bits right before it might look like
 * a valid chunk header by chance.
 */
bool
MemoryContextContains(MemoryContext context, void *pointer) {
       StandardChunkHeader *header;
       /*
        * Try to detect bogus pointers handed to us, poorly though we can.
        * Presumably, a pointer that isn't MAXALIGNED isn't pointing at an
        * allocated chunk.
        */
       if (pointer == NULL || pointer != (void *) MAXALIGN(pointer))
             return false;
       /*
        * OK, it's probably safe to look at the chunk header.
        */
       header = (StandardChunkHeader *)
             ((char *) pointer - STANDARDCHUNKHEADERSIZE);
       /*
        * If the context link doesn't match then we certainly have a
        * non-member chunk.  Also check for a reasonable-looking size as
        * extra guard against being fooled by bogus pointers.
        */
       if (header->context == context && AllocSizeIsValid(header->size))
             return true;
       return false; }
/*--------------------
 * MemoryContextCreate
 *         Context-type-independent part of context creation.
 *
 * This is only intended to be called by context-type-specific
 * context creation routines, not by the unwashed masses.
 *
 * The context creation procedure is a little bit tricky because
 * we want to be sure that we don't leave the context tree invalid
 * in case of failure (such as insufficient memory to allocate the
 * context node itself).  The procedure goes like this:
 *     1.  Context-type-specific routine first calls MemoryContextCreate(),
 *         passing the appropriate tag/size/methods values (the methods
 *         pointer will ordinarily point to statically allocated data).
 *         The parent and name parameters usually come from the caller.
 *     2.  MemoryContextCreate() attempts to allocate the context node,
 *         plus space for the name.  If this fails we can elog() with no
 *         damage done.
 *     3.  We fill in all of the type-independent MemoryContext fields.
 *     4.  We call the type-specific init routine (using the methods pointer).
 *         The init routine is required to make the node minimally valid
 *         with zero chance of failure --- it can't allocate more memory,
 *         for example.
 *     5.  Now we have a minimally valid node that can behave correctly
 *         when told to reset or delete itself.  We link the node to its
 *         parent (if any), making the node part of the context tree.
 *     6.  We return to the context-type-specific routine, which finishes
 *         up type-specific initialization.  This routine can now do things
 *         that might fail (like allocate more memory), so long as it's
 *         sure the node is left in a state that delete will handle.
 *
 * This protocol doesn't prevent us from leaking memory if step 6 fails
 * during creation of a top-level context, since there's no parent link
 * in that case.  However, if you run out of memory while you're building
 * a top-level context, you might as well go home anyway...
 *
 * Normally, the context node and the name are allocated from
 * TopMemoryContext (NOT from the parent context, since the node must
 * survive resets of its parent context!).     However, this routine is itself
 * used to create TopMemoryContext!  If we see that TopMemoryContext is NULL,
 * we assume we are creating TopMemoryContext and use malloc() to allocate
 * the node.
 *
 * Note that the name field of a MemoryContext does not point to
 * separately-allocated storage, so it should not be freed at context
 * deletion.
 *--------------------
 */
MemoryContext
MemoryContextCreate(NodeTag tag, Size size,
                         MemoryContextMethods *methods,
                         MemoryContext parent,
                         const char *name) {
       MemoryContext node;
       Size   needed = size + strlen(name) + 1;
       /* Get space for node and name */
       if (TopMemoryContext != NULL) {
             /* Normal case: allocate the node in TopMemoryContext */
             node = (MemoryContext) MemoryContextAlloc(TopMemoryContext,
                                                            needed); }
       else {
             /* Special case for startup: use good ol' malloc */
             node = (MemoryContext) malloc(needed);
             Assert(node != NULL); }
       /* Initialize the node as best we can */
       MemSet(node, 0, size);
       node->type = tag;
       node->methods = methods;
       node->parent = NULL;   /* for the moment */
       node->firstchild = NULL;
       node->nextchild = NULL;
       node->name = ((char *) node) + size;
       strcpy(node->name, name);
       /* Type-specific routine finishes any other essential initialization */
       (*node->methods->init) (node);
       /* OK to link node to parent (if any) */
       if (parent) {
             node->parent = parent;
             node->nextchild = parent->firstchild;
             parent->firstchild = node; }
       /* Return to type-specific creation routine to finish up */
       return node; }
/*
 * MemoryContextAlloc
 *         Allocate space within the specified context.
 *
 * This could be turned into a macro, but we'd have to import
 * nodes/memnodes.h into postgres.h which seems a bad idea.
 */
void *
MemoryContextAlloc(MemoryContext context, Size size) {
       AssertArg(MemoryContextIsValid(context));
       if (!AllocSizeIsValid(size))
             elog(ERROR, "MemoryContextAlloc: invalid request size %lu",
                   (unsigned long) size);
       return (*context->methods->alloc) (context, size); }
/*
 * pfree
 *         Release an allocated chunk.
 */
void
pfree(void *pointer) {
       StandardChunkHeader *header;
       /*
        * Try to detect bogus pointers handed to us, poorly though we can.
        * Presumably, a pointer that isn't MAXALIGNED isn't pointing at an
        * allocated chunk.
        */
       Assert(pointer != NULL);
       Assert(pointer == (void *) MAXALIGN(pointer));
       /*
        * OK, it's probably safe to look at the chunk header.
        */
       header = (StandardChunkHeader *)
             ((char *) pointer - STANDARDCHUNKHEADERSIZE);
       AssertArg(MemoryContextIsValid(header->context));
       (*header->context->methods->free_p) (header->context, pointer); }
/*
 * repalloc
 *
 */
void *
repalloc(void *pointer, Size size) {
       StandardChunkHeader *header;
       /*
        * Try to detect bogus pointers handed to us, poorly though we can.
        * Presumably, a pointer that isn't MAXALIGNED isn't pointing at an
        * allocated chunk.
        */
       Assert(pointer != NULL);
       Assert(pointer == (void *) MAXALIGN(pointer));
       /*
        * OK, it's probably safe to look at the chunk header.
        */
       header = (StandardChunkHeader *)
             ((char *) pointer - STANDARDCHUNKHEADERSIZE);
       AssertArg(MemoryContextIsValid(header->context));
       if (!AllocSizeIsValid(size))
             elog(ERROR, "repalloc: invalid request size %lu",
                   (unsigned long) size);
       return (*header->context->methods->realloc) (header->context,
                                                           pointer, size); }
/*
 * MemoryContextSwitchTo
 *         Returns the current context; installs the given context.
 */
MemoryContext
MemoryContextSwitchTo(MemoryContext context) {
       MemoryContext old;
       AssertArg(MemoryContextIsValid(context));
       old = CurrentMemoryContext;
       CurrentMemoryContext = context;
       return old; }
/*
 * MemoryContextStrdup
 *         Like strdup(), but allocate from the specified context
 */
char *
MemoryContextStrdup(MemoryContext context, const char *string) {
       char     *nstr;
       Size   len = strlen(string) + 1;
       nstr = (char *) MemoryContextAlloc(context, len);
       memcpy(nstr, string, len);
       return nstr; }
