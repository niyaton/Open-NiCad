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

namespace NVelocity.Runtime
{
	using System;
	using System.Runtime.Serialization;

	[Serializable]
	public class RuntimeException : System.Exception
	{
		public RuntimeException(string message) : base(message)
		{
		}

		public RuntimeException(string message, System.Exception innerException) : base(message, innerException)
		{
		}

		public RuntimeException(SerializationInfo info, StreamingContext context) : base(info, context)
		{
		}
	}
}