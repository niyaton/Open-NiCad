// Copyright 2004-2007 Castle Project - http://www.castleproject.org/
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

namespace Castle.DynamicProxy.Tests.GenClasses
{
	public class OnlyGenMethodsClass
	{
		private bool invoked;

		public bool Invoked
		{
			get { return invoked; }
		}

		public virtual Z DoSomething<Z>(Z z) where Z : new()
		{
			invoked = true;

			return new Z();
		}
	}
}