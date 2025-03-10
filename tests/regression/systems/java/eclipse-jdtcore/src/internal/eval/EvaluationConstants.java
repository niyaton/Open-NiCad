package org.eclipse.jdt.internal.eval;
/*
 * (c) Copyright IBM Corp. 2000, 2001.
 * All Rights Reserved.
 */
import org.eclipse.jdt.internal.compiler.util.CharOperation;
public interface EvaluationConstants {
       public static final char[] CODE_SNIPPET_CLASS_NAME_PREFIX = "CodeSnippet_".toCharArray(); //$NON-NLS-1$
       public static final char[] GLOBAL_VARS_CLASS_NAME_PREFIX = "GlobalVariables_".toCharArray(); //$NON-NLS-1$
       public static final char[] PACKAGE_NAME = "org.eclipse.jdt.internal.eval.target".toCharArray(); //$NON-NLS-1$
       public static final char[] CODE_SNIPPET_NAME = "org/eclipse/jdt/internal/eval/target/CodeSnippet".toCharArray(); //$NON-NLS-1$
       public static final char[] ROOT_CLASS_NAME = "CodeSnippet".toCharArray(); //$NON-NLS-1$
       public static final String ROOT_FULL_CLASS_NAME = new String(PACKAGE_NAME) + "." + new String(ROOT_CLASS_NAME); //$NON-NLS-1$
       public static final char[] SETRESULT_SELECTOR = "setResult".toCharArray(); //$NON-NLS-1$
       public static final char[] SETRESULT_ARGUMENTS = "Ljava.lang.Object;Ljava.lang.Class;".toCharArray(); //$NON-NLS-1$
       public static final char[][] ROOT_COMPOUND_NAME = CharOperation.arrayConcat(CharOperation.splitOn('.', PACKAGE_NAME), ROOT_CLASS_NAME);
       public static final String RUN_METHOD = "run"; //$NON-NLS-1$
       public static final String RESULT_VALUE_FIELD = "resultValue"; //$NON-NLS-1$
       public static final String RESULT_TYPE_FIELD = "resultType"; //$NON-NLS-1$
       public final static char[] LOCAL_VAR_PREFIX = "val$".toCharArray(); //$NON-NLS-1$
       public final static char[] DELEGATE_THIS = "val$this".toCharArray();  }//$NON-NLS-1$
