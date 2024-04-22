<template>
  <div class="description">
    <h1>Opis</h1>

    <section class="section">
      <h2>Korelacja</h2>
      <p>Korelacja to statystyczna miara związku między dwoma zmiennymi. Wartości korelacji wahają się od -1 do 1. Wartość 1 oznacza doskonałą korelację dodatnią, co oznacza, że zmienne poruszają się w tym samym kierunku, a wartość -1 oznacza doskonałą korelację ujemną, oznaczającą, że zmienne poruszają się w przeciwnych kierunkach. Wartość 0 oznacza brak korelacji, wskazując, że zmienne nie są ze sobą powiązane.</p>
    </section>

    <section class="section">
      <h2>Wskaźnik RSI (Relative Strength Index)</h2>
      <p>Wskaźnik RSI to narzędzie analizy technicznej wykorzystywane do pomiaru tempa zmian cen, pomagające określić warunki nadkupienia lub wyprzedania na rynku. Wartości RSI wahają się od 0 do 100. Ogólnie przyjmuje się, że wartości powyżej 70 wskazują na nadkupienie, a wartości poniżej 30 na wyprzedanie rynku.</p>
    </section>

    <section class="section">
      <h2>Dywergencja</h2>
      <p>Dywergencja występuje, gdy cena aktywa kieruje się w przeciwnym kierunku niż wskaźnik techniczny, taki jak RSI lub wskaźnik momentum. Jest to często interpretowane jako sygnał, że obecny trend cen może się odwrócić. Dywergencje mogą być zarówno „bycze” jak i „niedźwiedzie”.</p>
    </section>

    <section class="section">
      <h2>Bycza Dywergencja</h2>
      <p>Bycza dywergencja pojawia się, gdy cena aktywa osiąga nowe minimum, podczas gdy wskaźnik techniczny nie potwierdza tych minimów, tworząc wyższe dołki. To zjawisko może sugerować, że presja sprzedażowa słabnie i możliwy jest wzrost cen.</p>
    </section>

    <section class="section">
      <h2>Niedźwiedzia Dywergencja</h2>
      <p>Niedźwiedzia dywergencja ma miejsce, gdy cena aktywa osiąga nowe maksimum, ale wskaźnik techniczny nie tworzy nowego maksimum, tworząc niższe szczyty. Może to wskazywać na osłabienie trendu wzrostowego i potencjalny spadek cen.</p>
    </section>

    <section class="section">
      <h2>Dywergencja na RSI w stosunku do ceny</h2>
      <p>Specyficznie dla RSI, bycza dywergencja może pojawiać się podczas trendu spadkowego, gdy RSI zaczyna rosnąć, tworząc wyższe dołki, podczas gdy cena aktywa nadal tworzy niższe dołki. To może sygnalizować, że trend spadkowy traci na sile i może nastąpić odwrócenie. Niedźwiedzia dywergencja może wystąpić podczas trendu wzrostowego, gdy RSI zaczyna spadać, tworząc niższe szczyty, mimo że cena aktywa wciąż tworzy wyższe szczyty. To może wskazywać na możliwość nadchodzącej korekty lub odwrócenia trendu.</p>
    </section>
  </div>
</template>
  
  <script>
  export default {
    name: 'MainDescription',
  };
  </script>
  
  <style scoped>
.description {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.description h1 {
  text-align: center;
  color: #007BFF;
}

.section {
  margin-bottom: 20px;
  padding: 20px;
  border-left: 4px solid #007BFF;
  background-color: #f9f9f9;
}

.section h2 {
  color: #333;
  margin-bottom: 10px;
}

.section p {
  font-size: 16px;
  line-height: 1.6;
  text-align: justify;
}

</style>