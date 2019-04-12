<template>
  <div class= "flex-item" style="flex-basis: 500px"  id="app">
    <div class="error" v-for="e in errors" :key="e.message">{{e}}</div>
    <h1>Zeitgest</h1>
    <h2>{{question.content}}</h2>

    <div class="choices flex-container" v-if="!anwerPicked">
      <div class="choice" v-for="c in choices" :key="c" :question="question" >
        <div class="button" @click="pickAnswer(c)">
          {{c}}
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
      anwerPicked: false,
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
        this.question = { content: response.data.question, id: response.data.id }
        this.choices = Object.keys(response.data.answers)
        this.stats = response.data.answers
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
  flex-basis: 300px;
  max-width: 1000px;
}

.choices {
  justify-content: space-evenly;
}

.button {
  background-color: lightblue;
  padding: 5px;
  border-radius: 0.5em;
  min-width: 75px;
  max-width: 200px;
  height: auto;
  cursor: pointer;
}

.button:hover {
  background-color: rgb(132, 167, 179);
  color: white;
}

.error {
  color: red;
}

</style>
