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
    data: Object,
    answerPicked: String
  },
  components: {
    Chart
  },
  data () {
    return {
      chartOptions: {
        chart: {
          type: 'pie',
          backgroundColor: 'transparent'
        },
        title: {
          text: ''
        },
        series: [{
          name: 'Answers',
          colorByPoint: true,
          data: []
        }]
      }
    }
  },
  created () {
    this.chartOptions.series[0].data = Object.keys(this.data).map((choice) => {
      var score = this.data[choice]
      if (choice === this.answerPicked) {
        score++
      }
      return { name: choice, y: score }
    })
  }
}
</script>

<style scoped>

</style>
