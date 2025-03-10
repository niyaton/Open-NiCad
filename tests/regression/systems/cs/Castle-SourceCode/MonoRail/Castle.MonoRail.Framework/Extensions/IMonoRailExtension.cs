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

namespace Castle.MonoRail.Framework
{
	using System;
	using System.Xml;
	using Castle.Core;

	/// <summary>
	/// Contract for extensions that want to hook 
	/// on MonoRail's events
	/// </summary>
	/// <remarks>
	/// Extensions implementations must be thread safe and stateless.
	/// </remarks>
	public interface IMonoRailExtension : IServiceEnabledComponent
	{
		/// <summary>
		/// Gives to the extension implementor a chance to read 
		/// attributes and child nodes of the extension node
		/// </summary>
		/// <param name="node">The node that defines the MonoRail extension</param>
		void SetExtensionConfigNode(XmlNode node);
	}
}
