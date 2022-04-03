<script>
export default {
  methods: {
    changeOption(event) {
      document.querySelector('html').setAttribute('lang', event.target.value);
    },
  }
}
</script>

<template>
  <div class="language-switcher">
    <select v-model="$i18n.locale" @change="changeOption" class="form-select">
      <option value="en">English</option>
      <option value="ru">Русский</option>
      <option value="be">Беларуская</option>
      <option value="uk">Українська</option>
    </select>
  </div>
</template>

<style>
.language-switcher {
  width: 150px;
}
</style>
