<template>
  <div id="app">
    <div class="error" v-for="e in errors" :key="e">{{JSON.stringify}}</div>
    <h1>Zeitgest</h1>
    <h2>{{question}}</h2>
    <div v-if="!anwerPicked">
      <Choice v-for="c in choices" :key="c" @answer-picked="showStats()">{{c}}</Choice>
    </div>

    <Stats :data="stats" v-if="anwerPicked"/>
  </div>
</template>

<script>
import axios from 'axios'
import Choice from './components/Choice'
import Stats from './components/Stats'

const url =
  'https://6f079e8c-7090-4d70-a952-d40dbe3703f1.mock.pstmn.io/default/questions'

export default {
  name: 'App',
  components: {
    Choice,
    Stats
  },
  data () {
    return {
      question: '',
      choices: [],
      stats: {},
      anwerPicked: false,
      errors: []
    }
  },
  methods: {
    showStats () {
      this.anwerPicked = true
    }
  },
  created () {
    var that = this
    axios
      .get(url)
      .then(response => {
        that.question = response.data.question
        that.choices = Object.keys(response.data.answers)
        that.stats = response.data.answers
      })
      .catch(e => {
        this.errors.push(e)
      })
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
