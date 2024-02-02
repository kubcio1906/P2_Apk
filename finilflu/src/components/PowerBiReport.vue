<template>
    <div class="powerbi-report-container">
      <iframe
        class="powerbi-report-frame"
        :src="powerBiEmbedUrl"
        frameborder="0"
        allowFullScreen="true">
      </iframe>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PowerBiReport',
    data() {
      return {
        // W tym miejscu wklej kod osadzenia uzyskany z Power BI
        powerBiEmbedUrl: 'https://app.powerbi.com/reportEmbed?reportId=b2861cb7-1a57-4919-a05a-b16180aaf8f3&autoAuth=true&ctid=b7ed644a-d1b3-4946-85f9-30a3380c2618'
      };
    }
  }
  </script>
  
  <style>
  .powerbi-report-container {
    width: 100%;
    height: 600px; /* Możesz dostosować wysokość zgodnie z potrzebami */
    border: none;
    overflow: hidden;
  }
  
  .powerbi-report-frame {
    width: 100%;
    height: 100%;
    border: none;
  }
  </style>