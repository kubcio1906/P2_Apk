<template>
  <nav class="navbar">
    <div class="navbar-brand">
      
    </div>
    <ul class="navbar-nav">
      <li><router-link to="/">Strona Główna</router-link></li>
      <li><router-link to="/description">Opis</router-link></li>
     
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
  background-color: #333; 
  color: white;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between; 
  align-items: center;
}

.navbar-brand {
  font-size: 1.5em; 
  font-weight: bold;
}

.navbar-brand img {
  height: 40px; 
  margin-right: 10px;
}

.navbar-nav {
  list-style: none; 
  display: flex;
  margin: 0;
  padding: 0;
}

.navbar-nav li {
  margin-left: 20px; 
}

.navbar-nav a {
  color: white;
  text-decoration: none;
  font-size: 1.1em;
}

.navbar-nav a:hover {
  text-decoration: underline; 
}

.navbar-logo {
  height: 160px; 
  margin-right: 10px; 
}
</style>