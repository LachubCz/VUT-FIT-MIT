import React from 'react'
import Card from './Card'

const Hand = props =>  {
	if (props.turn === props.name) {
		return (
			<div id="Hand">
				<Card id="0" cardType={props.cards[0][0]} playable={props.cards[0][1]} playFunction={props.playF} discardFunction={props.discardF}/>
				<Card id="1" cardType={props.cards[1][0]} playable={props.cards[1][1]} playFunction={props.playF} discardFunction={props.discardF}/>
				<Card id="2" cardType={props.cards[2][0]} playable={props.cards[2][1]} playFunction={props.playF} discardFunction={props.discardF}/>
				<Card id="3" cardType={props.cards[3][0]} playable={props.cards[3][1]} playFunction={props.playF} discardFunction={props.discardF}/>
				<Card id="4" cardType={props.cards[4][0]} playable={props.cards[4][1]} playFunction={props.playF} discardFunction={props.discardF}/>
				<Card id="5" cardType={props.cards[5][0]} playable={props.cards[5][1]} playFunction={props.playF} discardFunction={props.discardF}/>
				<Card id="6" cardType={props.cards[6][0]} playable={props.cards[6][1]} playFunction={props.playF} discardFunction={props.discardF}/>
				<Card id="7" cardType={props.cards[7][0]} playable={props.cards[7][1]} playFunction={props.playF} discardFunction={props.discardF}/>
			</div>
		);
	}
	else {
		return (
			<div id="Hand">
				<Card />
				<Card />
				<Card />
				<Card />
				<Card />
				<Card />
				<Card />
				<Card />
			</div>
		);	
	}
}


export default Hand;