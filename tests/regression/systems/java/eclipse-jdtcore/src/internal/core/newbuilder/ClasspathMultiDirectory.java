package org.eclipse.jdt.internal.core.newbuilder;
/*
 * (c) Copyright IBM Corp. 2000, 2001.
 * All Rights Reserved.
 */
import org.eclipse.jdt.internal.compiler.env.NameEnvironmentAnswer;
class ClasspathMultiDirectory extends ClasspathDirectory {
String sourcePath; // includes .class files. The primary path is the source path
NameEnvironment nameEnvironment; // set at the beginning of each compile loop
ClasspathMultiDirectory(String sourcePath, String binaryPath) {
       super(binaryPath);
       this.sourcePath = sourcePath;
       if (!sourcePath.endsWith("/")) //$NON-NLS-1$
             this.sourcePath += "/";  }//$NON-NLS-1$
void cleanup() {
       super.cleanup();
       this.nameEnvironment = null; }
public boolean equals(Object o) {
       if (this == o) return true;
       if (!(o instanceof ClasspathMultiDirectory)) return false;
       ClasspathMultiDirectory md = (ClasspathMultiDirectory) o;
       return binaryPath.equals(md.binaryPath) && sourcePath.equals(md.sourcePath); }
NameEnvironmentAnswer findClass(char[] className, char[][] packageName) {
       if (nameEnvironment.additionalSourceFilenames != null) {
             // if an additional source file is waiting to be compiled, answer it
             // BUT not if this is a secondary type search,
             // if we answer the source file X.java which may no longer define Y
             // then the binary type looking for Y will fail & think the class path is wrong
             // let the recompile loop fix up dependents when Y has been deleted from X.java
             String sourceFilename = new String(className) + ".java"; //$NON-NLS-1$
             if (exists(sourcePath, sourceFilename, packageName)) {
                  String fullSourceName = sourcePath + NameEnvironment.assembleName(sourceFilename, packageName, '/');
                  String[] additionalSourceFilenames = nameEnvironment.additionalSourceFilenames;
                  for (int i = 0, l = additionalSourceFilenames.length; i < l; i++)
                      if (fullSourceName.equals(additionalSourceFilenames[i]))
                         return new NameEnvironmentAnswer(new SourceFile(fullSourceName, className, packageName)); } }
       // assume any class file found in this output folder would eventually be found...
       // its possible with multiple source folders, that a class file should not be found associated
       // with this source folder, but with another which we have yet to search
       return super.findClass(className, packageName); }
public String toString() {
       return "Source classpath directory " + sourcePath + //$NON-NLS-1$
             " with binary directory " + binaryPath;  } }//$NON-NLS-1$
