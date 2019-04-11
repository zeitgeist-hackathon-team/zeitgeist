<template>
  <div class="choice">
    <div class="button" @click="postAnswer()">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const url =
  'https://a36cdf41-e977-4921-af41-d18518bca27b.mock.pstmn.io/default/answers'

export default {
  name: 'Choice',
  data () {
    return {}
  },
  methods: {
    postAnswer () {
      this.$emit('answer-picked')
      axios.post(url)
        .catch(e => {
          this.errors.push(e)
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.button {
  cursor: pointer;
}

.button:hover {
  color: green;
}

.error {
  color: red;
}
</style>
