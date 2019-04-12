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
          type: 'pie'
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
    var vm = this
    vm.chartOptions.series[0].data = Object.keys(this.data).map((key) => {
      var val = vm.data[key]
      if (key === vm.answerPicked) {
        val++
      }
      return { name: key, y: val }
    })
  }
}
</script>

<style scoped>

</style>
