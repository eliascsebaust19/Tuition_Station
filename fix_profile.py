#!/usr/bin/env python3
import sys

html = r'''{% extends "base.html" %}

{% block title %}My Profile - Tuition Station{% endblock %}

{% block extra_css %}
<style>
body { margin: 0; background: var(--surface); }
.dashboard-layout { display: flex; min-height: 100vh; }

.sidebar {
    width: 260px;
    background: var(--surface-container-low);
    position: fixed; left: 0; top: 0;
    height: 100vh; display: flex; flex-direction: column;
    z-index: 100; padding: 1.5rem 0;
}
.sidebar-brand { padding: 0 1.5rem; margin-bottom: 2rem; text-align: center; }
.sidebar-brand h1 { font-size: 1.25rem; font-weight: 900; letter-spacing: -0.02em; color: var(--primary); }
.sidebar-brand p { font-size: 0.6rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; color: var(--secondary); margin-top: 0.25rem; }
.sidebar-nav { flex: 1; display: flex; flex-direction: column; gap: 0.25rem; padding: 0 0.75rem; }
.sidebar-nav a { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; border-radius: 0.75rem; color: var(--on-surface-variant); font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; transition: all 0.2s; text-decoration: none; }
.sidebar-nav a:hover { background: var(--surface-container-high); color: var(--on-surface); }
.sidebar-nav a.active { background: var(--secondary); color: var(--on-secondary); }
.sidebar-nav .material-symbols-outlined { font-size: 1.25rem; }
.sidebar-logout { padding: 0 0.75rem; margin-top: auto; }
.sidebar-logout a { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; border-radius: 0.75rem; color: var(--on-surface-variant); font-size: 0.875rem; font-weight: 600; text-decoration: none; transition: all 0.2s; }
.sidebar-logout a:hover { background: var(--surface-container-high); color: var(--error); }

.main-content { flex: 1; margin-left: 260px; padding: 2.5rem 3rem; max-width: calc(100vw - 260px); }
.page-header { margin-bottom: 2rem; }
.page-header h2 { font-size: 2rem; font-weight: 900; letter-spacing: -0.02em; }
.page-header p { color: var(--on-surface-variant); font-size: 0.9rem; margin-top: 0.25rem; }

.content-grid { display: grid; grid-template-columns: 320px 1fr; gap: 2rem; align-items: start; }

.profile-card {
    background: var(--surface-container-lowest);
    border-radius: 2rem; padding: 2.5rem 2rem;
    text-align: center; box-shadow: 0 4px 24px rgba(0,0,0,0.04);
    position: sticky; top: 2rem;
}
.profile-img-wrap {
    width: 140px; height: 140px; margin: 0 auto 1.25rem;
    border-radius: 50%; overflow: hidden;
    background: var(--surface-container);
    border: 4px solid var(--primary-fixed);
    cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
}
.profile-img-wrap:hover { transform: scale(1.03); box-shadow: 0 8px 30px rgba(0,74,198,0.15); }
.profile-img-wrap img { width: 100%; height: 100%; object-fit: cover; }
.profile-img-overlay {
    position: absolute; inset: 0;
    background: rgba(0,0,0,0.35);
    display: flex; align-items: center; justify-content: center;
    opacity: 0; transition: opacity 0.2s; border-radius: 50%;
}
.profile-img-wrap:hover .profile-img-overlay { opacity: 1; }
.profile-img-overlay .material-symbols-outlined { color: #fff; font-size: 2rem; }

.profile-card h3 { font-size: 1.25rem; font-weight: 800; margin-bottom: 0.25rem; }
.profile-card .role { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--on-surface-variant); opacity: 0.7; margin-bottom: 1rem; }
.status-pill {
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.5rem 1.25rem; border-radius: 9999px;
    font-size: 0.75rem; font-weight: 700;
    background: rgba(108,248,187,0.2);
    color: var(--on-secondary-container); margin-bottom: 1.5rem;
}
.status-pill .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--secondary); }
.btn-change-photo {
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.625rem 1.25rem; border-radius: 9999px;
    background: var(--surface-container-high); color: var(--on-surface);
    font-size: 0.75rem; font-weight: 700; border: none; cursor: pointer;
    transition: all 0.2s;
}
.btn-change-photo:hover { background: var(--primary); color: var(--on-primary); }
.quick-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 1.5rem; }
.quick-stat { background: var(--surface-container); border-radius: 1rem; padding: 1rem; }
.quick-stat .value { font-size: 1.25rem; font-weight: 800; color: var(--primary); }
.quick-stat .label { font-size: 0.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--on-surface-variant); margin-top: 0.25rem; }

.modal-overlay {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,0.45); backdrop-filter: blur(12px);
    z-index: 1000; align-items: center; justify-content: center;
}
.modal-overlay.active { display: flex; }
.modal-card {
    background: var(--surface-container-lowest); border-radius: 2rem;
    padding: 2.5rem; width: 100%; max-width: 420px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.15); text-align: center;
}
.modal-card h3 { font-size: 1.25rem; font-weight: 800; margin-bottom: 0.25rem; }
.modal-card p { font-size: 0.875rem; color: var(--on-surface-variant); margin-bottom: 1.5rem; }
.modal-card .file-drop {
    border: 2px dashed var(--outline-variant); border-radius: 1.5rem;
    padding: 2rem; margin-bottom: 1.5rem; cursor: pointer; transition: all 0.2s;
}
.modal-card .file-drop:hover { border-color: var(--primary); background: var(--surface-container-low); }
.modal-card .file-drop .material-symbols-outlined { font-size: 3rem; color: var(--outline); margin-bottom: 0.5rem; }
.modal-card .file-drop p { margin: 0; font-size: 0.875rem; color: var(--on-surface-variant); }
.modal-card .btn-upload {
    display: flex; align-items: center; justify-content: center; gap: 0.5rem;
    width: 100%; padding: 1rem; background: var(--primary); color: var(--on-primary);
    border: none; border-radius: 9999px; font-size: 0.875rem; font-weight: 700;
    cursor: pointer; transition: opacity 0.2s;
}
.modal-card .btn-upload:hover { opacity: 0.9; }
.modal-card .btn-close {
    margin-top: 0.75rem; background: transparent; color: var(--on-surface-variant);
    font-size: 0.875rem; font-weight: 600; border: none; cursor: pointer;
}

.form-card {
    background: var(--surface-container-lowest); border-radius: 2rem;
    padding: 2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 24px rgba(0,0,0,0.04);
}
.form-card h3 { font-size: 1rem; font-weight: 800; margin-bottom: 1.5rem; }
.form-grid-inner { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem 1.5rem; }
.form-group { margin-bottom: 0; }
.form-group.full { grid-column: 1 / -1; }
.form-group label { display: block; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--primary); margin-bottom: 0.5rem; }
.form-group input, .form-group select, .form-group textarea {
