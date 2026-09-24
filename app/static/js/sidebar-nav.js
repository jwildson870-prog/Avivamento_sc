(function(){
  'use strict';
  var body=document.body, toggle=document.querySelector('.sidebar-toggle');
  function open(){body.classList.add('sidebar-open'); if(toggle) toggle.setAttribute('aria-expanded','true');}
  function close(){body.classList.remove('sidebar-open'); if(toggle) toggle.setAttribute('aria-expanded','false');}
  if(toggle) toggle.addEventListener('click',function(){body.classList.contains('sidebar-open')?close():open();});
  document.querySelectorAll('[data-sidebar-close]').forEach(function(el){el.addEventListener('click',close);});
  document.querySelectorAll('[data-open-sidebar]').forEach(function(el){el.addEventListener('click',open);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape') close();});
  document.querySelectorAll('.side-section[data-section]').forEach(function(section){
    var key='avivamentoSidebarSections', saved={};
    try{saved=JSON.parse(localStorage.getItem(key))||{};}catch(e){}
    var name=section.getAttribute('data-section');
    if(Object.prototype.hasOwnProperty.call(saved,name)) section.open=!!saved[name];
    section.addEventListener('toggle',function(){try{saved[name]=section.open;localStorage.setItem(key,JSON.stringify(saved));}catch(e){}});
  });
})();
