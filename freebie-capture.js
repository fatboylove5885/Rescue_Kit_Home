/* What's For Eats shared freebie gate — 2026-10-28.
   Mobile-safe form state, verified Apps Script callbacks and an honest recovery path.
   Never regard a hidden iframe loading as proof a subscriber was recorded. */
(function(){
  "use strict";
  var BUSY_TIMEOUT_MS = 12000;
  function el(id){return document.getElementById(id);}
  function routeFor(asset){
    var routes=window.FREEBIE_HTML_ROUTES || {};
    var path=routes[asset] || "";
    if(typeof path!=="string" || !/^\/pdfs\/[a-z0-9-]+\.html$/.test(path)){return null;}
    return new URL(path,location.origin);
  }
  function hostnameAllowed(origin){
    try {
      var host=new URL(origin).hostname.toLowerCase();
      return host==="script.google.com" || host==="script.googleusercontent.com" ||
        host==="googleusercontent.com" || /\.googleusercontent\.com$/.test(host);
    }catch(e){return false;}
  }
  function setup(form,backend,frame,button,emailInput,marketingInput,messageBox,asset){
    if(!form||!backend||!frame||!button||!emailInput)return;
    var destination=routeFor(asset);
    if(!destination){return;}
    var active=false, timer=null, requestId="", startingLabel=button.textContent;
    var status=messageBox||document.createElement("div");
    if(!messageBox)form.appendChild(status);
    status.setAttribute("role","status");
    status.setAttribute("aria-live","polite");
    status.style.cssText="display:none;margin:12px 0;padding:12px 14px;border-radius:10px;background:#fff3e4;color:#563a28;font-size:15px;line-height:1.5;";
    var recovery=document.createElement("a");
    recovery.href=destination.pathname;
    recovery.textContent="Open your free printable directly →";
    recovery.style.cssText="display:none;margin:9px 0 12px;color:#2c694b;font-size:15px;text-decoration:underline;font-weight:700;";
    form.appendChild(recovery);
    function show(message,withLink){
      status.textContent=message;status.style.display="block";
      recovery.style.display=withLink?"inline-block":"none";
    }
    function finish(){
      active=false;
      if(timer){clearTimeout(timer);timer=null;}
      button.disabled=false;
      button.textContent=startingLabel;
      button.removeAttribute("aria-busy");
    }
    function validResponse(ev){
      var data=ev.data;
      if(!active||!data||data.type!=="freebie-signup-result"||!data.payload)return null;
      if(!hostnameAllowed(ev.origin))return null;
      // New Google Apps Script deployments include a one-time request ID.
      // Older responses are accepted only after confirming the exact local guide URL.
      if(data.requestId && data.requestId!==requestId)return null;
      var result=data.payload, target;
      try{target=new URL(result.url,location.origin);}catch(e){target=null;}
      if(result.ok && (!target || target.origin!==location.origin || target.pathname!==destination.pathname))return null;
      return result;
    }
    window.addEventListener("message",function(ev){
      var result=validResponse(ev);
      if(!result)return;
      finish();
      if(result.ok){
        show("Your free printable is ready. Opening it now…",true);
        window.location.assign(destination.href);
      }else{
        show((result.error||"We couldn't confirm the email request.")+" You can still open the free printable below.",true);
      }
    });
    // Google Apps Script's HtmlService can nest its reply inside additional iframes.
    // A completed load is not verified email delivery; it only lets us open
    // the free guide without trapping the visitor behind a stuck spinner.
    frame.addEventListener("load",function(){
      if(!active)return;
      setTimeout(function(){
        if(!active)return; // A real success/error callback already took priority.
        finish();
        show("Your request was submitted. Opening the free guide; please check your email for delivery confirmation.",true);
        window.location.assign(destination.href);
      },1800);
    });
    // Capture BEFORE all legacy form handlers, including inline listener fallbacks.
    form.addEventListener("submit",function(ev){
      ev.preventDefault();ev.stopImmediatePropagation();
      if(active)return;
      if(!form.reportValidity())return;
      var endpoint=window.FREEBIES_WEB_APP_URL||"";
      if(!/^https:\/\/script\.google\.com\/macros\/s\/[^/]+\/exec(?:\?.*)?$/.test(endpoint)){
        show("Email delivery is temporarily unavailable. You can still open your free printable below.",true);
        return;
      }
      if(!backend.elements.namedItem("email")||!backend.elements.namedItem("asset")){
        show("This signup form needs maintenance. You can open the free guide below.",true);
        return;
      }
      requestId="wfe-"+Date.now().toString(36)+"-"+Math.random().toString(36).slice(2,10);
      backend.action=endpoint;
      backend.target=frame.name||frame.id;
      backend.elements.namedItem("email").value=emailInput.value.trim();
      backend.elements.namedItem("asset").value=asset;
      if(backend.elements.namedItem("marketing"))backend.elements.namedItem("marketing").value=marketingInput&&marketingInput.checked?"true":"false";
      if(backend.elements.namedItem("source"))backend.elements.namedItem("source").value=location.href;
      var rid=backend.elements.namedItem("request_id");
      if(!rid){rid=document.createElement("input");rid.name="request_id";rid.type="hidden";backend.appendChild(rid);}
      rid.value=requestId;
      active=true;button.disabled=true;button.textContent="Sending your free printable…";
      button.setAttribute("aria-busy","true");
      show("Submitting your request securely. Your guide will open after confirmation.",false);
      timer=setTimeout(function(){
        if(!active)return;
        finish();
        show("We couldn't verify email delivery. Please try again, or open the free printable directly below.",true);
      },BUSY_TIMEOUT_MS);
      try { HTMLFormElement.prototype.submit.call(backend); }
      catch(err){finish();show("The email service didn't respond. Open your free printable below.",true);}
    },true);
  }
  function start(){
    var f=el("signup"),g=el("pdf-gate-form");
    if(f)setup(f,el("backend-form"),el("submit-frame"),el("submit"),el("email"),el("marketing"),el("error"),
      new URLSearchParams(location.search).get("asset")||"picky-family-7-night-dinner-plan");
    if(g){
      var asset=location.pathname.split("/").pop().replace(/\.html$/i,"");
      setup(g,el("pdf-gate-backend"),el("pdf-gate-frame"),el("pdf-gate-submit"),el("pdf-gate-email"),el("pdf-gate-marketing"),el("pdf-gate-error"),asset);
    }
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);
  else start();
})();
