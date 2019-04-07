$(document).ready(() => {
  let url = 'https://jqdrbwa4u7.execute-api.us-west-2.amazonaws.com/default/questions';
  //url = 'https://api.thecatapi.com/v1/breeds';


  const getResult = async () => {
    try {
      return await axios.get(url);
    } catch (error) {
      console.error(error);
    }
  };

  const getQuestions = async () => {
    const result = await getResult();

    if (result.data) {
      console.log(result.data);
    }

    let questionTitle = result.data.question;
    let choices = result.data.answers;

    choices.forEach((choice, i) => {
      console.log(i);
      let r = $(`<button class="${i}-button">
      <p class="${i}">${choice}</p>
      <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
        viewBox="0 0 512 512" enable-background="new 0 0 512 512" xml:space="preserve">
        <path id="paper-plane-icon" d="M462,54.955L355.371,437.187l-135.92-128.842L353.388,167l-179.53,124.074L50,260.973L462,54.955z
          M202.992,332.528v124.517l58.738-67.927L202.992,332.528z"></path>
      </svg>
    </button>`);
      $('.button-wrapper').append(r);

      $(`.${i}-button`).click(function () {
        $(this).toggleClass('clicked');
        $(`.${i}`).text((i, text) =>
          text === "Sent!" ? `${choice}` : "Sent!"
        );
        $("button").prop("disabled", true);
      });
    });

    $('h1').text(questionTitle);


  };

  getQuestions();
});