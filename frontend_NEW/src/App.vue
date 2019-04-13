<template>
  <div class="d-flex flex-column align-items-center" id="app">
    <div class="error" v-for="e in errors" :key="e.message">{{e}}</div>
    <h1 class="logo">Zeitgeist</h1>
    <div class="subtitle">The spirit of the time!</div>
    <div class="question outlined">{{question.content}}</div>

      <div class="choices-container" v-if="!anwerPicked">
      <div v-for="c in choices" :key="c" >
        <div class="choice-btn outlined d-flex flex-row justify-content-between" @click="pickAnswer(c)">
          <div>{{c}}</div>
          <i class="fa fa-paper-plane"></i>
        </div>
      </div>
    </div>

    <Stats class="stats" v-if="anwerPicked" :data="stats" :answer-picked="anwerPicked" />
  </div>
</template>

<script>
import axios from 'axios'
import Stats from './components/Stats'

const questionUrl = 'https://jqdrbwa4u7.execute-api.us-west-2.amazonaws.com/default/questions'
const answerUrl = 'https://omca46prfc.execute-api.us-west-2.amazonaws.com/default/answers'

export default {
  name: 'App',
  components: {
    Stats
  },
  data () {
    return {
      question: {},
      choices: [],
      stats: {},
      anwerPicked: '',
      errors: []
    }
  },
  methods: {
    pickAnswer (c) {
      this.anwerPicked = c

      var payload = {
        id: this.question.id,
        answers: [c]
      }

      axios.post(answerUrl, payload)
        .then(response => {
          console.log(response.status)
        })
        .catch(e => {
          this.errors.push(e)
        })
    }
  },
  created () {
    axios
      .get(questionUrl)
      .then(response => {
        this.question = { id: response.data.id, content: response.data.question }
        this.stats = response.data.answers
        this.choices = Object.keys(this.stats)
      })
      .catch(e => {
        this.errors.push(e)
      })
  }
}
</script>

<style>
.logo {
  font-family: 'Fair Prosper';
  font-size: 5.5em;
  margin-top: 50px;
}

.subtitle {
  font-weight: normal;
  font-size: 2em;
  margin-top: -20px;
  margin-right: -200px;
}

.question {
  font-size: 2.2em;
  text-align: center;
  margin-top: 100px;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  font-weight: bold;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  width: 50%;
  margin: auto;
}

.choices-container {
  margin-top: 50px;
  width: 100%;
}

.outlined {
  background-color: white;
  border: 2px black solid;
  border-radius: 10px;
  padding: 2px 10px;
  width: 100%;
}

.hoverable:hover {
  background-color: gray;
}

.choice-btn {
  margin-bottom: 20px;
  text-align: left;
  opacity: 0.9;
}

</style>
