package org.eclipse.jdt.internal.core.search.matching;
/*
 * (c) Copyright IBM Corp. 2000, 2001.
 * All Rights Reserved.
 */
import org.eclipse.jdt.core.IPackageFragmentRoot;
import org.eclipse.jdt.internal.compiler.util.HashtableOfObject;
import org.eclipse.jdt.internal.compiler.util.ObjectVector;
/**
 * A set of MatchingOPenables that is sorted by package fragment roots.
 */
public class MatchingOpenableSet {
       private HashtableOfObject rootsToOpenable = new HashtableOfObject(5);
       private int elementCount = 0;
       public void add(MatchingOpenable matchingOpenable) {
             IPackageFragmentRoot root = matchingOpenable.openable.getPackageFragmentRoot();
             char[] path = root.getPath().toString().toCharArray();
             ObjectVector openables = (ObjectVector)this.rootsToOpenable.get(path);
             if (openables == null) {
                  openables = new ObjectVector();
                  this.rootsToOpenable.put(path, openables);
                  openables.add(matchingOpenable);
                  this.elementCount++;
             } else if (!openables.contains(matchingOpenable)) {
                  openables.add(matchingOpenable);
                  this.elementCount++; } }
       public MatchingOpenable[] getMatchingOpenables(IPackageFragmentRoot[] roots) {
             MatchingOpenable[] result = new MatchingOpenable[this.elementCount];
             int index = 0;
             for (int i = 0, length = roots.length; i < length; i++) {
                  IPackageFragmentRoot root = roots[i];
                  char[] path = root.getPath().toString().toCharArray();
                  ObjectVector openables = (ObjectVector)this.rootsToOpenable.get(path);
                  if (openables != null) {
                      openables.copyInto(result, index);
                      index += openables.size(); } }
             if (index < this.elementCount) {
                  System.arraycopy(
                      result, 
                      0, 
                      result = new MatchingOpenable[index],
                      0,
                      index); }
             return result; } }
