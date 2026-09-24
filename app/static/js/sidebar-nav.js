(function () {
  'use strict';
  var key = 'avivamentoSidebarSections';
  function state() { try { return JSON.parse(localStorage.getItem(key)) || {}; } catch (e) { return {}; } }
  function save(s) { try { localStorage.setItem(key, JSON.stringify(s)); } catch (e) {} }
  document.addEventListener('DOMContentLoaded', function () {
    var sections = document.querySelectorAll('.side-section[data-section]');
    var saved = state();
    sections.forEach(function (section) {
      var name = section.getAttribute('data-section');
      if (Object.prototype.hasOwnProperty.call(saved, name)) section.open = !!saved[name];
      section.addEventListener('toggle', function () { var s = state(); s[name] = section.open; save(s); });
    });
  });
}());
