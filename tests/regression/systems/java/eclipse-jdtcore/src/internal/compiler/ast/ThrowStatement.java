package org.eclipse.jdt.internal.compiler.ast;
/*
 * (c) Copyright IBM Corp. 2000, 2001.
 * All Rights Reserved.
 */
import org.eclipse.jdt.internal.compiler.IAbstractSyntaxTreeVisitor;
import org.eclipse.jdt.internal.compiler.impl.*;
import org.eclipse.jdt.internal.compiler.codegen.*;
import org.eclipse.jdt.internal.compiler.flow.*;
import org.eclipse.jdt.internal.compiler.lookup.*;
public class ThrowStatement extends Statement {
       public Expression exception;
       public TypeBinding exceptionType;
       public ThrowStatement(Expression exception, int startPosition) {
             this.exception = exception;
             this.sourceStart = startPosition;
             this.sourceEnd = exception.sourceEnd; }
       public FlowInfo analyseCode(BlockScope currentScope, FlowContext flowContext, FlowInfo flowInfo) {
             exception.analyseCode(currentScope, flowContext, flowInfo);
             // need to check that exception thrown is actually caught somewhere
             flowContext.checkExceptionHandlers(exceptionType, this, flowInfo, currentScope);
             return FlowInfo.DeadEnd; }
       /**
        * Throw code generation
        *
        * @param currentScope org.eclipse.jdt.internal.compiler.lookup.BlockScope
        * @param codeStream org.eclipse.jdt.internal.compiler.codegen.CodeStream
        */
       public void generateCode(BlockScope currentScope, CodeStream codeStream) {
             if ((bits & IsReachableMASK) == 0)
                  return;
             int pc = codeStream.position;
             exception.generateCode(currentScope, codeStream, true);
             codeStream.athrow();
             codeStream.recordPositionsFrom(pc, this.sourceStart); }
       public void resolve(BlockScope scope) {
             exceptionType = exception.resolveTypeExpecting(scope, scope.getJavaLangThrowable());
             if (exceptionType == NullBinding
                      && scope.environment().options.complianceLevel <= CompilerOptions.JDK1_3){
                  // if compliant with 1.4, this problem will not be reported
                  scope.problemReporter().cannotThrowNull(this); }
             exception.implicitWidening(exceptionType, exceptionType); }
       public String toString(int tab) {
             String s = tabString(tab);
             s = s + "throw "; //$NON-NLS-1$
             s = s + exception.toStringExpression();
             return s; }
       public void traverse(IAbstractSyntaxTreeVisitor visitor, BlockScope blockScope) {
             if (visitor.visit(this, blockScope))
                  exception.traverse(visitor, blockScope);
             visitor.endVisit(this, blockScope); } }
