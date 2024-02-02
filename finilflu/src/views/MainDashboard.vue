<template>
  <div class="main-dashboard">
    <header class="app-header">
      <img src="../assets/logo.png" alt="Logo aplikacji" class="app-logo"/>
      <h1>Analiza Wpływu Inflacji i Stóp Procentowych USA na Rynki Światowe</h1>
    </header>
    <p class="app-description">
      Niniejsza aplikacja stanowi część projektu inżynierskiego badającego związki między kluczowymi wskaźnikami ekonomicznymi a zachowaniami rynkowymi.
      Zawiera ona zestaw interaktywnych wykresów i narzędzi analitycznych, które umożliwiają szczegółową analizę i śledzenie ruchów na rynkach finansowych.
    </p>
    <main class="content">
      <!-- Tutaj może być dynamiczna zawartość strony -->
    </main>
    <footer class="app-footer">
      <p>© 2024 Twoje Imię. Wszystkie prawa zastrzeżone.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'MainDashboard'
  // Tutaj możesz dodać logikę komponentu, jeśli jest potrzebna
}
</script>

<style scoped>
.main-dashboard {
  text-align: center;
}

.app-logo {
  width: 150px; /* Dostosuj rozmiar logo do swoich potrzeb */
}

.app-header {
  background-color: #333;
  padding: 20px;
  color: white;
}

.app-description {
  margin: 20px 0;
  color: #555;
}

.app-nav {
  margin-bottom: 20px;
}

.content {
  min-height: 600px; /* Wysokość sekcji z treścią */
}

.app-footer {
  background-color: #333;
  color: white;
  padding: 10px 0;
  position: absolute;
  bottom: 0;
  width: 100%;
}
</style>