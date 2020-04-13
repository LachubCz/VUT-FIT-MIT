import React from 'react';
import Card from './Card';

const Decks = props => {
	return (
		<div id="Decks">
			<Card showCard={true} />
			<Card cardType={props.playedCard} showCard={props.playable}/>
		</div>
	);
}

export default Decks;