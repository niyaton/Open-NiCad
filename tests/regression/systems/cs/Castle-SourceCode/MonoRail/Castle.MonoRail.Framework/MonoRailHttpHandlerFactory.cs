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
	using System.Web;
	using Castle.Core.Logging;

	/// <summary>
	/// Coordinates the creation of new <see cref="MonoRailHttpHandler"/> 
	/// and uses the configuration to obtain the correct factories 
	/// instances.
	/// </summary>
	public class MonoRailHttpHandlerFactory : IHttpHandlerFactory
	{
		private ILoggerFactory loggerFactory;

		/// <summary>
		/// Initializes a new instance of the <see cref="MonoRailHttpHandlerFactory"/> class.
		/// </summary>
		public MonoRailHttpHandlerFactory()
		{
		}

		/// <summary>
		/// Returns an instance of a class that implements 
		/// the <see cref="T:System.Web.IHttpHandler"></see> interface.
		/// </summary>
		/// <param name="context">An instance of the <see cref="T:System.Web.HttpContext"></see> class that provides references to intrinsic server objects (for example, Request, Response, Session, and Server) used to service HTTP requests.</param>
		/// <param name="requestType">The HTTP data transfer method (GET or POST) that the client uses.</param>
		/// <param name="url">The <see cref="P:System.Web.HttpRequest.RawUrl"></see> of the requested resource.</param>
		/// <param name="pathTranslated">The <see cref="P:System.Web.HttpRequest.PhysicalApplicationPath"></see> to the requested resource.</param>
		/// <returns>
		/// A new <see cref="T:System.Web.IHttpHandler"></see> object that processes the request.
		/// </returns>
		public virtual IHttpHandler GetHandler(HttpContext context, 
		                                       String requestType, 
		                                       String url, String pathTranslated)
		{
			if (!EngineContextModule.Initialized)
			{
				throw new RailsException("Looks like you forgot to register the http module " +
					typeof(EngineContextModule).FullName + "\r\nAdd '<add name=\"monorail\" type=\"Castle.MonoRail.Framework.EngineContextModule, Castle.MonoRail.Framework\" />' " +
					"to the <httpModules> section on your web.config");
			}

			IRailsEngineContext mrContext = EngineContextModule.ObtainRailsEngineContext(context);

			if (mrContext == null)
			{
				throw new RailsException("IRailsEngineContext is null. Looks like the " + 
					"EngineContextModule has not run for this request.");
			}

			return ObtainMonoRailHandler(mrContext);
		}

		/// <summary>
		/// Enables a factory to reuse an existing handler instance.
		/// </summary>
		/// <param name="handler">The <see cref="T:System.Web.IHttpHandler"></see> object to reuse.</param>
		public virtual void ReleaseHandler(IHttpHandler handler)
		{
			HttpContext httpContext = HttpContext.Current;

			if (httpContext != null)
			{
				IRailsEngineContext mrContext = EngineContextModule.ObtainRailsEngineContext(HttpContext.Current);

				if (mrContext != null)
				{
					IMonoRailHttpHandlerProvider provider = ObtainMonoRailHandlerProvider(mrContext);
					if (provider != null) provider.ReleaseHandler(handler);
				}
			}
		}

		private IHttpHandler ObtainMonoRailHandler(IRailsEngineContext mrContext)
		{
			IHttpHandler mrHandler = null;
			IMonoRailHttpHandlerProvider provider = ObtainMonoRailHandlerProvider(mrContext);

			if (provider != null)
			{
				mrHandler = provider.ObtainMonoRailHttpHandler(mrContext);
			}
			
			if (mrHandler == null)
			{
				ILogger logger = CreateLogger(typeof(MonoRailHttpHandler).FullName, mrContext);
				
				mrHandler = new MonoRailHttpHandler(logger);
			} 

			return mrHandler;
		}

		private IMonoRailHttpHandlerProvider ObtainMonoRailHandlerProvider(IRailsEngineContext mrContext)
		{
			return (IMonoRailHttpHandlerProvider) mrContext.GetService(typeof(IMonoRailHttpHandlerProvider));
		}

		/// <summary>
		/// This might be subject to race conditions, but
		/// I'd rather take the risk - which in the end
		/// means just replacing the instance - than
		/// creating locks that will affect every single request
		/// </summary>
		/// <param name="name">Logger name</param>
		/// <param name="provider">Service provider</param>
		/// <returns>Logger instance</returns>
		private ILogger CreateLogger(String name, IServiceProvider provider)
		{
			if (loggerFactory == null)
			{
				loggerFactory = (ILoggerFactory) provider.GetService(typeof(ILoggerFactory));
				
				if (loggerFactory == null)
				{
					loggerFactory = new NullLogFactory();
				}
			}
			
			return loggerFactory.Create(name);
		}
	}
}
