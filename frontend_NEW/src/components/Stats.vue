<template>
    <div>
      <Chart :options="chartOptions"/>
    </div>
</template>

<script>
import {Chart} from 'highcharts-vue'

export default {
  name: 'Stats',
  props: {
    data: Object
  },
  components: {
    Chart
  },
  data () {
    return {
      chartOptions: {
        series: [{
          name: 'Answers',
          colorByPoint: true,
          data: [{
            name: 'Chrome',
            y: 61.41,
            sliced: true,
            selected: true
          }, {
            name: 'Internet Explorer',
            y: 11.84
          }, {
            name: 'Firefox',
            y: 10.85
          }, {
            name: 'Edge',
            y: 4.67
          }, {
            name: 'Safari',
            y: 4.18
          }, {
            name: 'Other',
            y: 7.05
          }]
        }]
      }
    }
  }
}
</script>

<style scoped>

</style>
