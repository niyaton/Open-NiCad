//------------------------------------------------------------------------------
// <autogenerated>
//     This code was generated by a tool.
//     Runtime Version: 1.1.4322.2032
//
//     Changes to this file may cause incorrect behavior and will be lost if 
//     the code is regenerated.
// </autogenerated>
//------------------------------------------------------------------------------

// 
// This source code was auto-generated by Microsoft.VSDesigner, Version 1.1.4322.2032.
// 
namespace RssBandit.com.newsgator.services3 {
    using System.Diagnostics;
    using System.Xml.Serialization;
    using System;
    using System.Web.Services.Protocols;
    using System.ComponentModel;
    using System.Web.Services;
    
    
    /// <remarks/>
    [System.Diagnostics.DebuggerStepThroughAttribute()]
    [System.ComponentModel.DesignerCategoryAttribute("code")]
    [System.Web.Services.WebServiceBindingAttribute(Name="SubscriptionWebServiceSoap", Namespace="http://services.newsgator.com/svc/Subscription.asmx")]
    public class SubscriptionWebService : System.Web.Services.Protocols.SoapHttpClientProtocol {
        
        public NGAPIToken NGAPITokenValue;
        
        /// <remarks/>
        public SubscriptionWebService() {
            this.Url = "http://services.newsgator.com/ngws/svc/Subscription.asmx";
        }
        
        /// <remarks/>
        [System.Web.Services.Protocols.SoapHeaderAttribute("NGAPITokenValue")]
        [System.Web.Services.Protocols.SoapDocumentMethodAttribute("http://services.newsgator.com/svc/Subscription.asmx/AddSubscription", RequestNamespace="http://services.newsgator.com/svc/Subscription.asmx", ResponseNamespace="http://services.newsgator.com/svc/Subscription.asmx", Use=System.Web.Services.Description.SoapBindingUse.Literal, ParameterStyle=System.Web.Services.Protocols.SoapParameterStyle.Wrapped)]
        public int AddSubscription(string xmlUrl, int folderId, NGOSCredential cred) {
            object[] results = this.Invoke("AddSubscription", new object[] {
                        xmlUrl,
                        folderId,
                        cred});
            return ((int)(results[0]));
        }
        
        /// <remarks/>
        public System.IAsyncResult BeginAddSubscription(string xmlUrl, int folderId, NGOSCredential cred, System.AsyncCallback callback, object asyncState) {
            return this.BeginInvoke("AddSubscription", new object[] {
                        xmlUrl,
                        folderId,
                        cred}, callback, asyncState);
        }
        
        /// <remarks/>
        public int EndAddSubscription(System.IAsyncResult asyncResult) {
            object[] results = this.EndInvoke(asyncResult);
            return ((int)(results[0]));
        }
        
        /// <remarks/>
        [System.Web.Services.Protocols.SoapHeaderAttribute("NGAPITokenValue")]
        [System.Web.Services.Protocols.SoapDocumentMethodAttribute("http://services.newsgator.com/svc/Subscription.asmx/DeleteSubscriptions", RequestNamespace="http://services.newsgator.com/svc/Subscription.asmx", ResponseNamespace="http://services.newsgator.com/svc/Subscription.asmx", Use=System.Web.Services.Description.SoapBindingUse.Literal, ParameterStyle=System.Web.Services.Protocols.SoapParameterStyle.Wrapped)]
        public void DeleteSubscriptions(int[] subscriptionList) {
            this.Invoke("DeleteSubscriptions", new object[] {
                        subscriptionList});
        }
        
        /// <remarks/>
        public System.IAsyncResult BeginDeleteSubscriptions(int[] subscriptionList, System.AsyncCallback callback, object asyncState) {
            return this.BeginInvoke("DeleteSubscriptions", new object[] {
                        subscriptionList}, callback, asyncState);
        }
        
        /// <remarks/>
        public void EndDeleteSubscriptions(System.IAsyncResult asyncResult) {
            this.EndInvoke(asyncResult);
        }
        
        /// <remarks/>
        [System.Web.Services.Protocols.SoapHeaderAttribute("NGAPITokenValue")]
        [System.Web.Services.Protocols.SoapDocumentMethodAttribute("http://services.newsgator.com/svc/Subscription.asmx/ReplaceSubscriptions", RequestNamespace="http://services.newsgator.com/svc/Subscription.asmx", ResponseNamespace="http://services.newsgator.com/svc/Subscription.asmx", Use=System.Web.Services.Description.SoapBindingUse.Literal, ParameterStyle=System.Web.Services.Protocols.SoapParameterStyle.Wrapped)]
        public void ReplaceSubscriptions(string locationName, System.Xml.XmlElement opmlDocument) {
            this.Invoke("ReplaceSubscriptions", new object[] {
                        locationName,
                        opmlDocument});
        }
        
        /// <remarks/>
        public System.IAsyncResult BeginReplaceSubscriptions(string locationName, System.Xml.XmlElement opmlDocument, System.AsyncCallback callback, object asyncState) {
            return this.BeginInvoke("ReplaceSubscriptions", new object[] {
                        locationName,
                        opmlDocument}, callback, asyncState);
        }
        
        /// <remarks/>
        public void EndReplaceSubscriptions(System.IAsyncResult asyncResult) {
            this.EndInvoke(asyncResult);
        }
        
        /// <remarks/>
        [System.Web.Services.Protocols.SoapHeaderAttribute("NGAPITokenValue")]
        [System.Web.Services.Protocols.SoapDocumentMethodAttribute("http://services.newsgator.com/svc/Subscription.asmx/MergeSubscriptions", RequestNamespace="http://services.newsgator.com/svc/Subscription.asmx", ResponseNamespace="http://services.newsgator.com/svc/Subscription.asmx", Use=System.Web.Services.Description.SoapBindingUse.Literal, ParameterStyle=System.Web.Services.Protocols.SoapParameterStyle.Wrapped)]
        public System.Xml.XmlElement MergeSubscriptions(string locationName, System.Xml.XmlElement opmlDocument) {
            object[] results = this.Invoke("MergeSubscriptions", new object[] {
                        locationName,
                        opmlDocument});
            return ((System.Xml.XmlElement)(results[0]));
        }
        
        /// <remarks/>
        public System.IAsyncResult BeginMergeSubscriptions(string locationName, System.Xml.XmlElement opmlDocument, System.AsyncCallback callback, object asyncState) {
            return this.BeginInvoke("MergeSubscriptions", new object[] {
                        locationName,
                        opmlDocument}, callback, asyncState);
        }
        
        /// <remarks/>
        public System.Xml.XmlElement EndMergeSubscriptions(System.IAsyncResult asyncResult) {
            object[] results = this.EndInvoke(asyncResult);
            return ((System.Xml.XmlElement)(results[0]));
        }
        
        /// <remarks/>
        [System.Web.Services.Protocols.SoapHeaderAttribute("NGAPITokenValue")]
        [System.Web.Services.Protocols.SoapDocumentMethodAttribute("http://services.newsgator.com/svc/Subscription.asmx/MoveSubscription", RequestNamespace="http://services.newsgator.com/svc/Subscription.asmx", ResponseNamespace="http://services.newsgator.com/svc/Subscription.asmx", Use=System.Web.Services.Description.SoapBindingUse.Literal, ParameterStyle=System.Web.Services.Protocols.SoapParameterStyle.Wrapped)]
        public void MoveSubscription(int subscriptionId, int toFolderId) {
            this.Invoke("MoveSubscription", new object[] {
                        subscriptionId,
                        toFolderId});
        }
        
        /// <remarks/>
        public System.IAsyncResult BeginMoveSubscription(int subscriptionId, int toFolderId, System.AsyncCallback callback, object asyncState) {
            return this.BeginInvoke("MoveSubscription", new object[] {
                        subscriptionId,
                        toFolderId}, callback, asyncState);
        }
        
        /// <remarks/>
        public void EndMoveSubscription(System.IAsyncResult asyncResult) {
            this.EndInvoke(asyncResult);
        }
        
        /// <remarks/>
        [System.Web.Services.Protocols.SoapHeaderAttribute("NGAPITokenValue")]
        [System.Web.Services.Protocols.SoapDocumentMethodAttribute("http://services.newsgator.com/svc/Subscription.asmx/RenameSubscription", RequestNamespace="http://services.newsgator.com/svc/Subscription.asmx", ResponseNamespace="http://services.newsgator.com/svc/Subscription.asmx", Use=System.Web.Services.Description.SoapBindingUse.Literal, ParameterStyle=System.Web.Services.Protocols.SoapParameterStyle.Wrapped)]
        public void RenameSubscription(int subscriptionId, string newName) {
            this.Invoke("RenameSubscription", new object[] {
                        subscriptionId,
                        newName});
        }
        
        /// <remarks/>
        public System.IAsyncResult BeginRenameSubscription(int subscriptionId, string newName, System.AsyncCallback callback, object asyncState) {
            return this.BeginInvoke("RenameSubscription", new object[] {
                        subscriptionId,
                        newName}, callback, asyncState);
        }
        
        /// <remarks/>
        public void EndRenameSubscription(System.IAsyncResult asyncResult) {
            this.EndInvoke(asyncResult);
        }
        
        /// <remarks/>
        [System.Web.Services.Protocols.SoapHeaderAttribute("NGAPITokenValue")]
        [System.Web.Services.Protocols.SoapDocumentMethodAttribute("http://services.newsgator.com/svc/Subscription.asmx/GetSubscriptionCounts", RequestNamespace="http://services.newsgator.com/svc/Subscription.asmx", ResponseNamespace="http://services.newsgator.com/svc/Subscription.asmx", Use=System.Web.Services.Description.SoapBindingUse.Literal, ParameterStyle=System.Web.Services.Protocols.SoapParameterStyle.Wrapped)]
        public System.Xml.XmlElement GetSubscriptionCounts(string location) {
            object[] results = this.Invoke("GetSubscriptionCounts", new object[] {
                        location});
            return ((System.Xml.XmlElement)(results[0]));
        }
        
        /// <remarks/>
        public System.IAsyncResult BeginGetSubscriptionCounts(string location, System.AsyncCallback callback, object asyncState) {
            return this.BeginInvoke("GetSubscriptionCounts", new object[] {
                        location}, callback, asyncState);
        }
        
        /// <remarks/>
        public System.Xml.XmlElement EndGetSubscriptionCounts(System.IAsyncResult asyncResult) {
            object[] results = this.EndInvoke(asyncResult);
            return ((System.Xml.XmlElement)(results[0]));
        }
        
        /// <remarks/>
        [System.Web.Services.Protocols.SoapHeaderAttribute("NGAPITokenValue")]
        [System.Web.Services.Protocols.SoapDocumentMethodAttribute("http://services.newsgator.com/svc/Subscription.asmx/GetSubscriptionList", RequestNamespace="http://services.newsgator.com/svc/Subscription.asmx", ResponseNamespace="http://services.newsgator.com/svc/Subscription.asmx", Use=System.Web.Services.Description.SoapBindingUse.Literal, ParameterStyle=System.Web.Services.Protocols.SoapParameterStyle.Wrapped)]
        public System.Xml.XmlElement GetSubscriptionList(string location, string syncToken) {
            object[] results = this.Invoke("GetSubscriptionList", new object[] {
                        location,
                        syncToken});
            return ((System.Xml.XmlElement)(results[0]));
        }
        
        /// <remarks/>
        public System.IAsyncResult BeginGetSubscriptionList(string location, string syncToken, System.AsyncCallback callback, object asyncState) {
            return this.BeginInvoke("GetSubscriptionList", new object[] {
                        location,
                        syncToken}, callback, asyncState);
        }
        
        /// <remarks/>
        public System.Xml.XmlElement EndGetSubscriptionList(System.IAsyncResult asyncResult) {
            object[] results = this.EndInvoke(asyncResult);
            return ((System.Xml.XmlElement)(results[0]));
        }
        
        /// <remarks/>
        [System.Web.Services.Protocols.SoapDocumentMethodAttribute("http://services.newsgator.com/svc/Subscription.asmx/GetUpdates", RequestNamespace="http://services.newsgator.com/svc/Subscription.asmx", ResponseNamespace="http://services.newsgator.com/svc/Subscription.asmx", Use=System.Web.Services.Description.SoapBindingUse.Literal, ParameterStyle=System.Web.Services.Protocols.SoapParameterStyle.Wrapped)]
        public string[] GetUpdates(string locationName, string syncToken, out string newToken) {
            object[] results = this.Invoke("GetUpdates", new object[] {
                        locationName,
                        syncToken});
            newToken = ((string)(results[1]));
            return ((string[])(results[0]));
        }
        
        /// <remarks/>
        public System.IAsyncResult BeginGetUpdates(string locationName, string syncToken, System.AsyncCallback callback, object asyncState) {
            return this.BeginInvoke("GetUpdates", new object[] {
                        locationName,
                        syncToken}, callback, asyncState);
        }
        
        /// <remarks/>
        public string[] EndGetUpdates(System.IAsyncResult asyncResult, out string newToken) {
            object[] results = this.EndInvoke(asyncResult);
            newToken = ((string)(results[1]));
            return ((string[])(results[0]));
        }
    }
    
    /// <remarks/>
    [System.Xml.Serialization.XmlTypeAttribute(Namespace="http://services.newsgator.com/svc/Subscription.asmx")]
    [System.Xml.Serialization.XmlRootAttribute(Namespace="http://services.newsgator.com/svc/Subscription.asmx", IsNullable=false)]
    public class NGAPIToken : System.Web.Services.Protocols.SoapHeader {
        
        /// <remarks/>
        public string Token;
    }
    
    /// <remarks/>
    [System.Xml.Serialization.XmlTypeAttribute(Namespace="http://services.newsgator.com/svc/Subscription.asmx")]
    public class Credential {
        
        /// <remarks/>
        public string username;
        
        /// <remarks/>
        public string passwordenc;
        
        /// <remarks/>
        public string domain;
    }
    
    /// <remarks/>
    [System.Xml.Serialization.XmlTypeAttribute(Namespace="http://services.newsgator.com/svc/Subscription.asmx")]
    public class NGOSCredential {
        
        /// <remarks/>
        [System.Xml.Serialization.XmlElementAttribute("networkCredential", typeof(Credential))]
        [System.Xml.Serialization.XmlElementAttribute("useNGOSCredentials", typeof(object))]
        public object Item;
    }
}
