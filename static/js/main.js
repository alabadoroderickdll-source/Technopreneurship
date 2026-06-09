/* CareerSync - Main JavaScript */

document.addEventListener('DOMContentLoaded', function () {

  // ── Dark Mode Toggle ──────────────────────────────────────────
  const darkToggle = document.getElementById('darkToggle');
  const body = document.body;
  const storedTheme = localStorage.getItem('cs-theme') || 'light';

  function applyTheme(theme) {
    body.setAttribute('data-theme', theme);
    if (darkToggle) {
      darkToggle.innerHTML = theme === 'dark'
        ? '<i class="bi bi-sun-fill"></i>'
        : '<i class="bi bi-moon-fill"></i>';
    }
    localStorage.setItem('cs-theme', theme);
  }

  applyTheme(storedTheme);

  if (darkToggle) {
    darkToggle.addEventListener('click', function () {
      const current = body.getAttribute('data-theme');
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  // ── Active Nav Link ────────────────────────────────────────────
  const navLinks = document.querySelectorAll('.cs-nav-link');
  const currentPath = window.location.pathname;
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ── Sidebar Active Link ────────────────────────────────────────
  const sideLinks = document.querySelectorAll('.cs-sidenav a');
  sideLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ── Auto-dismiss Alerts ────────────────────────────────────────
  const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // ── Progress Bar Animation ─────────────────────────────────────
  const progressBars = document.querySelectorAll('[data-width]');
  progressBars.forEach(bar => {
    const width = bar.getAttribute('data-width');
    setTimeout(() => {
      bar.style.width = width + '%';
    }, 200);
  });

  // ── Interview Current Checkbox ─────────────────────────────────
  const isCurrentCheckbox = document.getElementById('id_is_current');
  const endDateField = document.getElementById('id_end_date');
  if (isCurrentCheckbox && endDateField) {
    function toggleEndDate() {
      endDateField.disabled = isCurrentCheckbox.checked;
      if (isCurrentCheckbox.checked) {
        endDateField.value = '';
        endDateField.placeholder = 'Present';
      }
    }
    isCurrentCheckbox.addEventListener('change', toggleEndDate);
    toggleEndDate();
  }

  // ── Skill Suggestions ─────────────────────────────────────────
  const skillInput = document.getElementById('id_name');
  const commonSkills = [
    'Python', 'Django', 'JavaScript', 'React', 'SQL', 'Excel',
    'Communication', 'Teamwork', 'Leadership', 'Problem Solving',
    'HTML/CSS', 'Node.js', 'Java', 'PHP', 'MySQL', 'Customer Service',
    'Sales', 'Data Analysis', 'Microsoft Office', 'Time Management',
    'TypeScript', 'Vue.js', 'PostgreSQL', 'Git', 'Docker', 'AWS'
  ];

  if (skillInput) {
    const datalist = document.createElement('datalist');
    datalist.id = 'skill-suggestions';
    commonSkills.forEach(skill => {
      const opt = document.createElement('option');
      opt.value = skill;
      datalist.appendChild(opt);
    });
    document.body.appendChild(datalist);
    skillInput.setAttribute('list', 'skill-suggestions');
  }

  // ── Confirm Deletes ─────────────────────────────────────────────
  const deleteButtons = document.querySelectorAll('[data-confirm]');
  deleteButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
      const msg = this.getAttribute('data-confirm') || 'Are you sure?';
      if (!confirm(msg)) e.preventDefault();
    });
  });

  // ── Smooth Scroll Anchors ──────────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Counter Animation ──────────────────────────────────────────
  function animateCounter(el, target, duration = 1500) {
    let start = 0;
    const step = target / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= target) { start = target; clearInterval(timer); }
      el.textContent = Math.floor(start).toLocaleString();
    }, 16);
  }

  const counters = document.querySelectorAll('[data-counter]');
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        animateCounter(el, parseInt(el.getAttribute('data-counter')));
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(counter => counterObserver.observe(counter));

  // ── Salary Display ─────────────────────────────────────────────
  function formatSalary(n) {
    if (n >= 1000) return '₱' + (n / 1000).toFixed(0) + 'K';
    return '₱' + n;
  }

  // ── Tooltip Init ──────────────────────────────────────────────
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach(el => new bootstrap.Tooltip(el));

  // ── Popover Init ─────────────────────────────────────────────
  const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
  popovers.forEach(el => new bootstrap.Popover(el));

  console.log('%c🚀 CareerSync loaded', 'color: #2563EB; font-weight: bold; font-size: 14px');
});
