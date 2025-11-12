<script setup>
import MainPage from './components/MainPage.vue'
</script>

<template>
  <nav class="top-menu">
    <a href="#" class="menu-link">Главная</a>
    <a href="#" class="menu-link">По датам</a>
  </nav>
  <MainPage />
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
</style>
