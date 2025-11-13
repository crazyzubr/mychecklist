<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <nav class="top-menu">
    <RouterLink to="/" class="menu-link" exact>Главная</RouterLink>
    <RouterLink to="/by-dates" class="menu-link">По датам</RouterLink>
  </nav>
  <RouterView />
</template>

<style>
:root {
  color-scheme: light !important;
}

.top-menu {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background-color: #f0f0f0;
  border-bottom: 1px solid #ccc;
}

.menu-link {
  text-decoration: none;
  color: #213547;
  font-weight: bold;
  cursor: pointer;
}

.menu-link:hover {
  color: #747bff;
}

.menu-link.router-link-exact-active {
  text-decoration: underline;
}
</style>
