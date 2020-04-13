import React from 'react';
import {
	Route,
	withRouter
} from 'react-router-dom'

import './App.css';
import Config from './config.js';
import PlayerStats from './components/PlayerStats'
import CastleVisual from './components/CastleVisual'
import Hand from './components/Hand'
import Decks from './components/Decks'
import Card from './components/Card'

import Aplaus from './sound/aplaus.mp3'
import BouraniHradby from './sound/bourani_hradby.mp3'
import BouraniHradu from './sound/bourani_hradu.mp3'
import Fanfary from './sound/fanfary.mp3'
import Karta from './sound/karta.mp3'
import KletbaSound from './sound/kletba.mp3'
import Ptaci from './sound/ptaci.mp3'
import SnizeniZasob from './sound/snizeni_zasob.mp3'
import StaveniHradby from './sound/staveni_hradby.mp3'
import StaveniHradu from './sound/staveni_hradu.mp3'
import ZvyseniSily from './sound/zvyseni_sily.mp3'
import ZvyseniZasob from './sound/zvyseni_zasob.mp3'


var socket = new WebSocket('ws://' + Config.host + ':' + Config.port);
var newStateUpdated = false;
var game_end = false;

class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			formState: "none",
			beforeInitStateMsg: true,
			playerName: "",
			opponentName: "",
			gameID: "",
			playerStats: {},
			opponentStats: {},
			turn: "",
			playedCardPlayable: true,
			lastPlayedCardPlayable: true,
			cardsPlayed: 0,
			newStateUpdated: false
		}

		this.processReceivedMessage = this.processReceivedMessage.bind(this);
		this.processEndMessage = this.processEndMessage.bind(this);
		this.getPlayerStats = this.getPlayerStats.bind(this);
		this.getOpponentStats = this.getOpponentStats.bind(this);


		this.renderForm = this.renderForm.bind(this);

		this.showNameInForm = this.showNameInForm.bind(this);
		this.showWholeForm = this.showWholeForm.bind(this);
		this.handleNameChange = this.handleNameChange.bind(this);
		this.handleGameIDChange = this.handleGameIDChange.bind(this);
		this.handleFormSubmit = this.handleFormSubmit.bind(this);
		
		this.updateCastlePosition = this.updateCastlePosition.bind(this);
		this.animateCastle = this.animateCastle.bind(this);
		this.updateWallPosition = this.updateWallPosition.bind(this);
		this.animateWall = this.animateWall.bind(this);

		this.playCard = this.playCard.bind(this);
		this.playCardSound = this.playCardSound.bind(this);

		this.discardCard = this.discardCard.bind(this);
		this.announceWinner = this.announceWinner.bind(this);
	}

	componentDidMount() {
		game_end = false;

		// Listen for messages
		socket.addEventListener('message', this.processReceivedMessage);
		socket.addEventListener('close', this.processEndMessage);

		if (this.state.beforeInitStateMsg === true) {
			this.props.history.push('/');
		}
	}

	getOpponentNameFromGameState(gameState) {
		let name1 = gameState.player_1_status.name;
		let name2 = gameState.player_2_status.name;
		return name1 !== this.state.playerName ? name1 : name2;
	}

	getPlayerStats(gameState) {
		let state1 = gameState.player_1_status;
		let state2 = gameState.player_2_status;
		return state1.name === this.state.playerName ? state1 : state2;
	}

	getOpponentStats(gameState) {
		let state1 = gameState.player_1_status;
		let state2 = gameState.player_2_status;
		return state1.name === this.state.opponentName ? state1 : state2;
	}

	processEndMessage(event) {
		if (!game_end) {
			alert("Spojení přerušeno, je potřeba začít znovu, obnovte stránku.\nPřetrvává-li problém, nahlašte nám to!");
			window.location.reload(true);	
		}
	}

	async processReceivedMessage(event) {
		//console.log('Message from server ', event.data);
		let data = JSON.parse(event.data);
		switch(data.type) {
		    // game_id
		    case 2:
		    	//console.log("Processing GameID message.");
		    	this.setState({ gameID: data.game_id });
		    	break;
		    
		    // game state
		    case 3:
		    // game end
		    case 5:
		    	if (data.type === 5) {
		    		game_end = true;
		    	}
		    	// add opponent to state if waiting / joining
		    	// redirect to /play if waiting / joining
		    	if (this.state.beforeInitStateMsg === true) {
		    		this.setState({
		    			beforeInitStateMsg: false,
		    			turn: data.content.game_status,
		    			opponentName: this.getOpponentNameFromGameState(data.content),
		    			playerStats: this.getPlayerStats(data.content),
		    			opponentStats: this.getOpponentStats(data.content)
		    		});
		    		// set game state
		    		this.props.history.push('/play');
		    	}
		    	else {
			    	// determine castle change
			    	let playerStats = this.getPlayerStats(data.content);
			    	let opponentStats = this.getOpponentStats(data.content);
			    	
			    	let new_player_castle = playerStats.stats.estate.castle;
			    	let new_opponent_castle = opponentStats.stats.estate.castle;
			    	
			    	let old_player_castle = this.state.playerStats.stats.estate.castle;
			    	let old_opponent_castle = this.state.opponentStats.stats.estate.castle;

			    	let new_player_wall = playerStats.stats.estate.wall;
			    	let new_opponent_wall = opponentStats.stats.estate.wall;

			    	let old_player_wall = this.state.playerStats.stats.estate.wall;
			    	let old_opponent_wall = this.state.opponentStats.stats.estate.wall;

			    	let last_played_card = data.content.last_played_card[0];
			    	let last_card_not_discarded = data.content.last_played_card[1] === "played";

			    	var any_castle_lower = (new_player_castle < old_player_castle) || 
			    		(new_opponent_castle < old_opponent_castle);

			    	// update last pplayed card
			    	this.setState({playedCard: last_played_card});
			    	this.setState({playedCardPlayable: last_card_not_discarded});

			    	// play card animation
			    	await this.animatePlayedCard();	

			    	// set last played card playable
			    	this.setState({lastPlayedCard: last_played_card});
			    	this.setState({lastPlayedCardPlayable: last_card_not_discarded});

			    	// perform change sound / animation
			    	if (last_card_not_discarded) {
			    		this.playCardSound(last_played_card, any_castle_lower);
			    	}

			    	// change castles / walls if needed
			    	this.animateCastle("Left", old_player_castle, new_player_castle);
			    	this.animateCastle("Right", old_opponent_castle, new_opponent_castle);

			    	this.animateWall("Left", old_player_wall, new_player_wall);
			    	this.animateWall("Right", old_opponent_wall, new_opponent_wall);

			    	// set state to rerender
			    	await this.setState({
			    		playerStats: playerStats,
			    		opponentStats: opponentStats
			    	});

			    	// animate new card depending on if I played or my opponent todo
			    	await this.animateNewCard();

			    	// change turn in order to change hand
			    	let cards_played = this.state.cardsPlayed
			    	if (cards_played < 2) {
			    		await this.setState({
			    			turn: data.content.game_status,
			    			cardsPlayed: cards_played + 1
			    		})
			    	}

			    	if (cards_played >= 1) {
			    		newStateUpdated = true;
			    	}
			    	
			    	// show all cards in hand
			    	Array.from(document.getElementById('Hand').childNodes).map(card => card.style.opacity = "1");

			    	// on game end
			    	if (data.type === 5) {
			    		console.log("Processing End message");
				
			    		// celebration of the right side
			    		if (data.content.game_status === this.state.playerName) {
			    			// black castle win
			    			alert('Black a.k.a YOU WON!');
			    			this.announceWinner("Left");
			    		}
			    		else {
			    			// red castle win
			    			alert('Red a.k.a YOUR OPPONENT WON!');
			    			this.announceWinner("Right");
			    		}
			    	}
		    	};
		    	break;
		    
		    // material update
		    case 7:
		    	//while(!this.state.newStateUpdated) {
		    	while(!newStateUpdated) {
		    		await new Promise(r => setTimeout(r, 200));
			   	}

		    	await this.setState({
		    		turn: data.content.game_status,
		    		playerStats: this.getPlayerStats(data.content),
		    		opponentStats: this.getOpponentStats(data.content),
		    	});
		    	newStateUpdated = false;
		    	break;

			default:
				//console.log("Received unexpected message: " + data);
				break;
		}
	}

	async announceWinner(side) {
		let trumpet = document.getElementById("Castle" + side).getElementsByClassName("CastleTrumpet")[0];

		this.setState({turn: ""});
		// show trumpeter
		trumpet.style.display = "initial";
		
		// play fanfary
		await this.playCardSound("fanfary");

		await new Promise(r => setTimeout(r, 3000));

		// play celebration
		await this.playCardSound("aplaus");
		
		// show celebrating ants
		document.getElementById("Celebration" + side).style.display = "initial";
	}

	async animateNewCard() {
		var card = document.getElementById("NewCard");
		var top;
		var left;
		
		// display card
		card.style.display = "initial";

		for (let i = 0; i < 50; i++) {
			top = i;
			left = (0.1122449 * i) + 40.88776;
			card.style.top = top + "vh";
			card.style.left = left + "vw";
			await new Promise(r => setTimeout(r, 20));
		}

		// hide card and reposition
		card.style.display = "none";
		card.style.top = 0;
		card.style.left = "41vw";
	}

	async animatePlayedCard() {
		var card = document.getElementById("PlayedCard");
		var top;
		var left;
		
		// display card
		card.style.display = "initial";

		// play card sound
		this.playCardSound("karta");

		for (let i = 0; i < 50; i++) {
			left = 0.1122449*i + 46.5;
			top = 50 - i;
			card.style.top = top + "vh";
			card.style.left = left + "vw";
			await new Promise(r => setTimeout(r, 20));
		}

		// hide card and reposition
		card.style.display = "none";
		card.style.top = "50vh";
		card.style.left = "46.5vw";
	}

	updateCastlePosition(elem, val) {
		let x = (val > 100) ? 100 : val;
		let bottom_val = (1.95*x) - 100;
		let clip_path_val = (-0.8*x) + 80;
		elem.style.bottom = bottom_val + "px";
		elem.style.clipPath = "inset(0 0 " + clip_path_val + "% 0)";
	}
	
	async animateCastle(side, old_val, new_val) {
		// get correct castle (CastleLeft or CastleRight)
		let castle = document.getElementById('Castle' + side);

		// act based on animation direction
		if (new_val > old_val) {
			while (old_val < new_val) {
				this.updateCastlePosition(castle, old_val);
				old_val++;
				await new Promise(r => setTimeout(r, 10));
			}
		}
		else if (new_val < old_val){
			new Audio(BouraniHradu).play();
			while (old_val > new_val) {
				this.updateCastlePosition(castle, old_val);
				old_val--;
				await new Promise(r => setTimeout(r, 10));
			}	
		}
	}

	updateWallPosition(elem, val) {
		let bottom_val = 1.979798*val - 101.9798;
		let clip_path_val = 89.89899 - 0.8989899*val;
		elem.style.bottom = bottom_val + "px";
		elem.style.clipPath = "inset(0 0 " + clip_path_val + "% 0)";
	}

	async animateWall(side, old_val, new_val) {
		// get correct wall (WallLeft or WallRight)
		var wall = document.getElementById('Wall' + side);

		// act based on direction
		if (new_val > old_val) {
			new Audio(StaveniHradby).play();
			while (new_val > old_val) {
				this.updateWallPosition(wall, old_val);
				old_val++;
				await new Promise(r => setTimeout(r, 10));
			}
		}
		else if (new_val < old_val) {
			new Audio(BouraniHradby).play();
			while (old_val > new_val) {
				this.updateWallPosition(wall, old_val);
				old_val--;
				await new Promise(r => setTimeout(r, 10));
			}
		}

		if (new_val === 0) {
			wall.style.clipPath = "inset(0 0 " + 100 + "% 0)";
		}
	}

	renderForm() {
		if (this.state.formState === "create game") {
			return (
				<form id="SignInGameForm" onSubmit={this.handleFormSubmit}>
					<label>
						Tvoje jméno:
						<input type="text" value={this.state.playerName} onChange={this.handleNameChange} pattern="[a-zA-Z0-9]+" name="playerName" title="Use only letters and numbers" required />
					</label>
					<button id="FormSubmit" type="submit">Pojďme na to!</button>
				</form>
			);
		}
		else if (this.state.formState === "join game") {
			return (
				<form id="SignInGameForm" onSubmit={this.handleFormSubmit}>
					<label>
						Tvoje jméno:
						<input type="text" value={this.state.playerName} onChange={this.handleNameChange} pattern="[a-zA-Z0-9]+" name="playerName" title="Use only letters and numbers"  required />
					</label>
					<label>
						ID hry:
						<input id="GameIDInput" type="text" value={this.state.gameID} onChange={this.handleGameIDChange} pattern="[a-zA-Z0-9]+" name="gameID" title="Use only letters and numbers"  required />
					</label>
					<button id="FormSubmit" type="submit">Pojďme na to!</button>
				</form>
			);
		}
		else {
			return <form />;
		}
	}

	showNameInForm() {
		this.setState({ formState: "create game" });
	}

	showWholeForm() {
		this.setState({ formState: "join game" });
	}

	handleNameChange(event) {
		this.setState({playerName: event.target.value});
	}

	handleGameIDChange(event) {
		this.setState({gameID: event.target.value});
	}

	handleFormSubmit(event) {
		event.preventDefault();
		
		// create game
		if (document.getElementById('GameIDInput') === null) {
			socket.send(JSON.stringify({"type": 0, "content": this.state.playerName}));
		}
		// join game
		else {
			socket.send(JSON.stringify({"type": 1, "content": this.state.playerName, "game_id": this.state.gameID}));
		}

		this.props.history.push('/loading');
	}

	async playCardSound(card_name, any_castle_lower=false) {
		switch (card_name) {
			case "ceta":
			case "jezdec":
			case "rytir":
			case "smrtka":
			case "strelec":
			case "ztec":
			case "drak":
				if (any_castle_lower) {
					new Audio(BouraniHradu).play();
				}
				else {
					new Audio(BouraniHradby).play();
				}
				break;

			case "swat":
				new Audio(BouraniHradu).play(); break;

			case "kletba":
				new Audio(KletbaSound).play(); break;

			case "saboter":
			case "znic_cihly":
			case "znic_krystaly":
			case "znic_zbrane":
				new Audio(SnizeniZasob).play(); break;

			case "hradba":
			case "obrana":
			case "zed":
				new Audio(StaveniHradby).play(); break;
			
			case "skritci":
			case "babylon":
			case "pevnost":
			case "povoz": 
			case "rezervy":
			case "vez":
			case "zaklady":
				new Audio(StaveniHradu).play(); break;
			
			case "skola":
			case "nabor":
			case "carodej":
				new Audio(ZvyseniSily).play(); break;
			

			case "caruj_cihly":
			case "caruj_krystaly":
			case "caruj_zbrane":
			case "zlodej":
				new Audio(ZvyseniZasob).play(); break;

			case "fanfary":
				await new Audio(Fanfary).play(); break;

			case "aplaus":
				await new Audio(Aplaus).play(); break;

			default:
				new Audio(Karta).play(); break;
		}
	}

	async playCard(cardIndex) {
		let card = document.getElementById('Hand').childNodes[cardIndex];

		card.style.opacity = "0";

		// send
		socket.send(JSON.stringify({
			"type": 4,
			"content": Number(cardIndex),
			"game_id": this.state.gameID
		}));
	}

	async discardCard(cardIndex) {
		let card = document.getElementById('Hand').childNodes[cardIndex];

		card.style.opacity = "0";

		// send
		socket.send(JSON.stringify({
			"type": 6,
			"content": Number(cardIndex),
			"game_id": this.state.gameID
		}));
	}

	render() {
		if (this.state.beforeInitStateMsg === true) {
			return (
				<div className="App">
					<Route path="/play">
					</Route>

					<Route path="/loading">
						<div id="LoadingPageContent">
							<p>Čekáme na tvého protivníka</p>
							<p>ID hry: <b>{this.state.gameID}</b></p>
							<div className="loader">
								<div></div>
								<div></div>
								<div></div>
							</div>
						</div>
					</Route>

					<Route exact path="/">
						<div id="MainPageElems">
							<div id="FormTypeButtons">
								<button type="button" onClick={this.showNameInForm}>Vytvoř hru</button>
								<button type="button" onClick={this.showWholeForm}>Připoj se</button>
							</div>

							{this.renderForm()}
						</div>
					</Route>
				</div>
			);
		}

		return (
			<div className="App">

				<Route path="/play">
					{/*<button id="ClickItButton" onClick={this.animatePlayedCard} >Click ittt</button>*/}

					{/*<Card id="NewCard" cardType={this.state.playedCard} showCard={true} />*/}
					<Card id="NewCard" cardType="" showCard={true} />
					<Card id="PlayedCard" cardType={this.state.playedCard} showCard={this.state.playedCardPlayable} />
					<Decks playedCard={this.state.lastPlayedCard}  playable={this.state.lastPlayedCardPlayable} />
					
					<div className="PlayerHalf">
						<PlayerStats name={this.state.playerName} stats={this.state.playerStats.stats} />
						<CastleVisual side="left" estateStats={this.state.playerStats.stats.estate} />
					</div>
					<div className="PlayerHalf">
						<CastleVisual side="right" estateStats={this.state.opponentStats.stats.estate} />
						<PlayerStats name={this.state.opponentName} stats={this.state.opponentStats.stats} />
					</div>

					<Hand cards={this.state.playerStats.hand} turn={this.state.turn} name={this.state.playerName} playF={this.playCard} discardF={this.discardCard} />	

				</Route>

				<Route path="/loading">
					<div id="LoadingPageContent">
						<p>Čekáme na tvého protivníka</p>
						<p>ID hry: <b>{this.state.gameID}</b></p>
						<div className="loader">
							<div></div>
							<div></div>
							<div></div>
						</div>
					</div>
				</Route>

				<Route exact path="/">
					<div id="MainPageElems">
						<div id="FormTypeButtons">
							<button type="button" onClick={this.showNameInForm}>Vytvoř hru</button>
							<button type="button" onClick={this.showWholeForm}>Připoj se</button>
						</div>

						{this.renderForm()}
					</div>
				</Route>

			</div>
		);
	}
}

export default withRouter(App);
