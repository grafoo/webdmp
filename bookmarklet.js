javascript:(
  function(){
    window.location.href = "http://localhost:9999/bookmark?url=" +
      encodeURIComponent(window.location.href.split('?')[0]) +
      "&name=" + encodeURIComponent(document.title);
  }
)();
