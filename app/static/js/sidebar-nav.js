(function () {
  'use strict';
  var key = 'avivamentoSidebarSections';

  function state() {
    try { return JSON.parse(localStorage.getItem(key)) || {}; } catch (e) { return {}; }
  }
  function save(s) {
    try { localStorage.setItem(key, JSON.stringify(s)); } catch (e) {}
  }

  document.addEventListener('DOMContentLoaded', function () {
    var sidebar = document.getElementById('app-sidebar');
    var toggle = document.getElementById('sidebar-toggle');
    var close = document.getElementById('sidebar-close');
    var backdrop = document.getElementById('sidebar-backdrop');
    var sections = document.querySelectorAll('.side-section[data-section]');
    var saved = state();

    sections.forEach(function (section) {
      var name = section.getAttribute('data-section');
      if (Object.prototype.hasOwnProperty.call(saved, name)) section.open = !!saved[name];
      section.addEventListener('toggle', function () {
        var s = state();
        s[name] = section.open;
        save(s);
      });
    });

    if (!sidebar || !toggle || !close || !backdrop) return;

    function openSidebar() {
      sidebar.classList.add('is-open');
      sidebar.setAttribute('aria-hidden', 'false');
      toggle.setAttribute('aria-expanded', 'true');
      backdrop.hidden = false;
      document.body.classList.add('sidebar-open');
    }

    function closeSidebar() {
      sidebar.classList.remove('is-open');
      sidebar.setAttribute('aria-hidden', 'true');
      toggle.setAttribute('aria-expanded', 'false');
      backdrop.hidden = true;
      document.body.classList.remove('sidebar-open');
    }

    toggle.addEventListener('click', openSidebar);
    close.addEventListener('click', closeSidebar);
    backdrop.addEventListener('click', closeSidebar);
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && sidebar.classList.contains('is-open')) closeSidebar();
    });

    sidebar.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.matchMedia('(max-width: 900px)').matches) closeSidebar();
      });
    });
  });
}());
