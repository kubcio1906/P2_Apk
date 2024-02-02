<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <img src="../assets/mojelogo.png" alt="Logo"> <!-- Logo Twojej aplikacji -->
    </div>
    <ul class="navbar-nav">
      <li><router-link to="/">Strona Główna</router-link></li>
      <li><router-link to="/markets">Rynki</router-link></li>
      <li><router-link to="/analysis">Analizy</router-link></li>
      <!-- Linki logowania/wylogowania tutaj -->
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar'
}
</script>
  
  <style>
.navbar {
  background-color: #333; /* Ciemny tło paska nawigacyjnego */
  color: white;
  padding: 10px 20px; /* Odstępy wewnątrz paska nawigacyjnego */
  display: flex;
  justify-content: space-between; /* Rozmieszczenie elementów na pasku */
  align-items: center;
}

.navbar-brand {
  font-size: 1.5em; /* Wielkość czcionki dla marki/tytułu */
  font-weight: bold;
}

.navbar-brand img {
  height: 40px; /* Wysokość logo, dostosuj według potrzeb */
  margin-right: 10px;
}

.navbar-nav {
  list-style: none; /* Usunięcie kropek z listy */
  display: flex;
  margin: 0;
  padding: 0;
}

.navbar-nav li {
  margin-left: 20px; /* Odstępy między elementami listy */
}

.navbar-nav a {
  color: white;
  text-decoration: none; /* Usunięcie podkreślenia z linków */
  font-size: 1.1em;
}

.navbar-nav a:hover {
  text-decoration: underline; /* Podkreślenie linku po najechaniu */
}

.navbar-logo {
  height: 160px; /* Dostosuj wysokość loga */
  margin-right: 10px; /* Odstęp od innych elementów w navbarze */
}
</style>