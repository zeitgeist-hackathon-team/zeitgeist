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
          data: []
        }]
      }
    }
  },
  created () {
    var vm = this
    vm.chartOptions.series[0].data = Object.keys(this.data).map((key) => {
      return { name: key, y: vm.data[key] }
    })
  }
}
</script>

<style scoped>

</style>
