package org.eclipse.jdt.internal.compiler.codegen;
import org.eclipse.jdt.internal.compiler.AbstractSyntaxTreeVisitorAdapter;
import org.eclipse.jdt.internal.compiler.ast.BranchStatement;
import org.eclipse.jdt.internal.compiler.ast.DoStatement;
import org.eclipse.jdt.internal.compiler.ast.ForStatement;
import org.eclipse.jdt.internal.compiler.ast.LabeledStatement;
import org.eclipse.jdt.internal.compiler.ast.SwitchStatement;
import org.eclipse.jdt.internal.compiler.ast.WhileStatement;
import org.eclipse.jdt.internal.compiler.lookup.BlockScope;
public class ResetStateForCodeGenerationVisitor
       extends AbstractSyntaxTreeVisitorAdapter {
       public boolean visit(SwitchStatement statement, BlockScope scope) {
             statement.resetStateForCodeGeneration();
             return true; }
       public boolean visit(ForStatement forStatement, BlockScope scope) {
             forStatement.resetStateForCodeGeneration();
             return true; }
       public boolean visit(WhileStatement whileStatement, BlockScope scope) {
             whileStatement.resetStateForCodeGeneration();
             return true; }
       public boolean visit(LabeledStatement labeledStatement, BlockScope scope) {
             labeledStatement.resetStateForCodeGeneration();
             return true; }
       public boolean visit(DoStatement doStatement, BlockScope scope) {
             doStatement.resetStateForCodeGeneration();
             return true; }
       public boolean visit(BranchStatement branchStatement, BlockScope scope) {
             branchStatement.resetStateForCodeGeneration();
             return true; } }
