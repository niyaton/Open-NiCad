package org.eclipse.jdt.internal.compiler.env;
/*
 * (c) Copyright IBM Corp. 2000, 2001.
 * All Rights Reserved.
 */
import org.eclipse.jdt.internal.compiler.*;
public interface ISourceMethod extends IGenericMethod {
/**
 * Answer the unresolved names of the argument types
 * or null if the array is empty.
 *
 * A name is a simple name or a qualified, dot separated name.
 * For example, Hashtable or java.util.Hashtable.
 */
char[][] getArgumentTypeNames();
/**
 * Answer the source end position of the method's declaration.
 */
int getDeclarationSourceEnd();
/**
 * Answer the source start position of the method's declaration.
 */
int getDeclarationSourceStart();
/**
 * Answer the unresolved names of the exception types
 * or null if the array is empty.
 *
 * A name is a simple name or a qualified, dot separated name.
 * For example, Hashtable or java.util.Hashtable.
 */
char[][] getExceptionTypeNames();
/**
 * Answer the source end position of the method's selector.
 */
int getNameSourceEnd();
/**
 * Answer the source start position of the method's selector.
 */
int getNameSourceStart();
/**
 * Answer the unresolved name of the return type
 * or null if receiver is a constructor or clinit.
 *
 * The name is a simple name or a qualified, dot separated name.
 * For example, Hashtable or java.util.Hashtable.
 */
char[] getReturnTypeName(); }
