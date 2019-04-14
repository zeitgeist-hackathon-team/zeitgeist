<template>
  <div class="d-flex flex-column align-items-center justify-content-around" id="app">
    <div class="error" v-for="e in errors" :key="e.message">{{e}}</div>
    <!-- <div>
      <h1 class="logo">Zeitgeist</h1>
      <div class="subtitle">The spirit of the time</div>
    </div> -->
    <div class="question">{{question.content}}</div>

    <div class="choices-container" v-if="!showChart">
      <div v-for="c in choices" :key="c" >
        <div class="choice card d-flex flex-row justify-content-between align-items-center" @click="pickAnswer(c)">
          <div>{{c}}</div>
          <i class="fa fa-paper-plane" :class="{fly: answerPicked == c}"></i>
        </div>
      </div>
    </div>

    <Stats class="stats" v-if="showChart" :data="stats" :answer-picked="answerPicked" />

    <div id="post-btn"
      title="Post new question"
      class="btn btn-success"
      @click="showModal = true">
      <i class="fa fa-plus"></i>
    </div>

    <Modal v-if="showModal" @cancel="showModal = false" @post="postQuestion">
      <h3 slot="header">Post New Question</h3>
      <PostQuestion/>
      <div slot="btn-text">Post <i class="fa fa-paper-plane"></i></div>
    </Modal>
  </div>
</template>

<script>
import axios from 'axios'
import Stats from './components/Stats'
import Modal from './components/Modal'
import PostQuestion from './components/PostQuestion'

const questionUrl = 'https://jqdrbwa4u7.execute-api.us-west-2.amazonaws.com/default/questions'
const answerUrl = 'https://omca46prfc.execute-api.us-west-2.amazonaws.com/default/answers'

export default {
  name: 'App',
  components: {
    Stats,
    PostQuestion,
    Modal
  },
  data () {
    return {
      question: {},
      choices: [],
      stats: {},
      answerPicked: '',
      errors: [],
      showChart: false,
      showModal: false
    }
  },
  methods: {
    pickAnswer (c) {
      this.answerPicked = c

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

      setTimeout(() => { this.showChart = true }, 800)
    },
    postQuestion (event) {
      this.showModal = false
      alert('blah')
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
  },
  mounted () {
    this.$root.$on('add-update-question', question => {
      window.console.log(question)
    })
  }
}
</script>

<style>
.logo {
  font-size: 2.0em;
  margin-top: 50px;
}

.subtitle {
  font-weight: normal;
  font-size: 1.5em;
  /* todo change font family */
}

.question {
  font-size: 2.2em;
  text-align: center;
  margin-top: 50px;
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

.card {
  background-color: white;
  padding: 2px 10px;
  border-radius: 0;
  box-shadow: 0 0 3px lightgray;
  width: 100%;
  transition: all .09s ease-in-out;
}

.card:hover {
  transform: scale(1.09);
  background-color: rgb(230, 230, 230);
}

.choice {
  margin-bottom: 10px;
  text-align: left;
  position: relative;
}

@keyframes fly-animation {
  from {
    left: 0px;
    bottom: 0px;
    }
  to {
    left: 100px;
    bottom: 50px;
    opacity: 0;
  }
}

.fly {
  position: relative;
  animation-name: fly-animation;
  animation-duration: 0.8s;
  animation-timing-function: ease-out
}

#post-btn {
  position: fixed;
  right: 5px;
  top: 5px;
}

</style>
