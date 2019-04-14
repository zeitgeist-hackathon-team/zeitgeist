<template>
  <SurveyBuilder :options="config"/>
</template>

<script>
import { SurveyBuilder } from 'vue-survey-builder'

export default {
  components: {
    SurveyBuilder
  },
  data () {
    return {
      config: {
        id: null,
        question: null,
        type: null,
        multiSelect: false,
        characterLimited: false,
        hasMinMax: false,
        allowDecimals: false,
        sequence: null,
        minValue: 1,
        maxValue: 1,
        labels: [],
        dateFormat: 'MM/DD/YYYY',
        timeFormat: '12',
        intervals: 2,
        textLimit: 1024,
        units: null,
        options: [
          {
            body: null,
            sequence: 1
          },
          {
            body: null,
            sequence: 2
          }
        ]
      }
    }
  }
}
</script>

<style>
</style>
