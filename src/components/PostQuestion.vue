<template>
  <form>
    <div class="form-group">
      <label for="question">The Question</label>
      <textarea id="question" class="form-control" v-model="theQuestion.question"></textarea>
      <small id="questionHelp" class="form-text text-muted">This better be a good question</small>
    </div>
    <div class="form-row" v-for="(answer, i) in theQuestion.answers" :key="i">
      <div class="col-2"><label :for="`answer-${i}`">Answer {{i + 1}}</label></div>
      <div class="col-9">
        <input :id="`answer-${i}`" type="text" class="form-control" v-model="theQuestion.answers[i]">
      </div>
      <div class="col-1">
        <i
          v-if="theQuestion.answers.length > 2"
          class="btn btn-danger fa fa-times"
          @click="removeAnswer(i)"
        ></i>
      </div>
    </div>
    <div class="form-group">
      <i class="btn btn-success fa fa-plus" @click="addAnswer('')"></i>
    </div>
    <div class="modal-footer">
      <div class="btn btn-danger" @click="$emit('cancel')">Cancel</div>
      <div class="btn btn-success" @click="emitQuestion">
        <slot name="btn-text">Post Question</slot>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  components: {},
  data () {
    return {
      theQuestion: { question: '', answers: ['', ''] }
    }
  },
  methods: {
    addAnswer (a) {
      this.theQuestion.answers.push(a)
    },
    removeAnswer (i) {
      this.theQuestion.answers.splice(i, 1)
    },
    emitQuestion () {
      var q = this.theQuestion
      q.answers = this.uniqNonEmpty(q.answers)
      if (q.question && q.answers && q.answers.length) {
        this.$emit('post', q)
      }
    },
    uniqNonEmpty (a) {
      var seen = {}
      return a.filter(item => {
        return (!item || seen.hasOwnProperty(item)) ? false : (seen[item] = true)
      })
    }
  }
}
</script>

<style>
.form-row {
  margin-bottom: 5px;
}
</style>
