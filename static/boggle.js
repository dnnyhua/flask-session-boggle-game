class BoggleGame {
	constructor(game_length = 60) {
		this.usedWords = new Set();
		this.totalScore = 0;
		this.game_length = game_length;

		this.timer = setInterval(this.updateTimer.bind(this), 1000);

		$("#form-add-word").on("submit", this.handleSubmitWord.bind(this));
		
	}

	showWord(validWord){
		$(".wordsList").append($(`<li>${validWord}</li>`));
	
	}

	showScore() {
		$(".score").text(this.totalScore);
	}

	showMessage(msg, cls) {
		$(".msg").text(msg).removeClass().addClass(`msg ${cls}`);
	}

	async handleSubmitWord(evt) {
		evt.preventDefault();

		// retrieve the word that was submitted on the form
		let $inputWord = $(".inputWord");
		let inputWord = $inputWord.val().toLowerCase();

		// return if blank submission is made
		if (!inputWord) return;

		// check if the word is used already
		if (this.usedWords.has(inputWord)) {
			this.showMessage(
				`${inputWord} has been used already. Please enter a different word.`, 'red');
			$(".inputWord").val("").focus();
			return;
		}

		// need to check server to see if inputWord is valid. Will need to route to '/check-word'
		const resp = await axios.get("/check-submitted-word", {
			params: { inputWord: inputWord },
		});
		if (resp.data.result === "not-word") {
			this.showMessage(`${inputWord} is not a valid word`,'red');
		} else if (resp.data.result === "not-on-board") {
			this.showMessage(`${inputWord} is not on the board`, 'red');
		} else {
			this.usedWords.add(inputWord);
			this.totalScore += inputWord.length;
			this.showScore();
			this.showMessage(`${inputWord} is a valid word`, 'green');
			this.showWord(inputWord);
		}

		// clear the input field on the form
		$(".inputWord").val("").focus();
	}

	async updateTimer(){
		this.game_length -= 1;
		$('.timer').text(this.game_length);

		if(this.game_length === 0){
			clearInterval(this.timer);
			await this.gameResult();
		}
	}


	// update post game info
	async gameResult(){
		// hide the form
		$('#form-add-word').hide();
		const resp = await axios.post('/post-score', {score: this.totalScore});
		// If the high score was beaten
		if(resp.data.brokeRecord){
			this.showMessage(`New Record: ${this.totalScore}`, 'green');	
		// If high score was not beaten
		}else {
			this.showMessage(`Final Score: ${this.totalScore}`, 'green');
		}
	}	
}








