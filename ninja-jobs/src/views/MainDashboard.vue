<template>
  <div class="main-dashboard">
    <header class="app-header">
      <img src="../assets/lolo.png" alt="Logo aplikacji" class="app-logo"/>
      <h1>Analiza Wpływu Inflacji i Stóp Procentowych USA na Rynki Światowe</h1>
    </header>
    <p class="app-description">
      Niniejsza aplikacja stanowi część projektu inżynierskiego badającego związki między kluczowymi wskaźnikami ekonomicznymi a zachowaniami rynkowymi.
      Zawiera ona zestaw interaktywnych wykresów i narzędzi analitycznych, które umożliwiają szczegółową analizę i śledzenie ruchów na rynkach finansowych.
    </p>
   
    <iframe class="powerbi-iframe" :src="powerBiEmbedUrl" frameborder="0" allowFullScreen="true"></iframe>
    <main class="content">
      
    </main>
    <footer class="app-footer">
      <p>© 2024 Jakub Madej. Wszystkie prawa zastrzeżone.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'MainDashboard',
  data() {
    return {
      powerBiEmbedUrl: 'https://app.powerbi.com/reportEmbed?reportId=b2861cb7-1a57-4919-a05a-b16180aaf8f3&autoAuth=true&ctid=b7ed644a-d1b3-4946-85f9-30a3380c2618'
    };
  }
}
</script>

<style scoped>

.app-logo {
  width: 100px; 
  height: auto; 
}


.powerbi-iframe {
  width: 100%; 
  height: 600px; 
}
</style>