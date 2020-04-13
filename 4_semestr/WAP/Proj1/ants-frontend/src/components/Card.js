import React from 'react'

import Babylon from '../img/cards/building/babylon.png'
import Hradba from '../img/cards/building/hradba.png'
import Obrana from '../img/cards/building/obrana.png'
import Pevnost from '../img/cards/building/pevnost.png'
import Povoz from '../img/cards/building/povoz.png'
import Rezervy from '../img/cards/building/rezervy.png'
import Skola from '../img/cards/building/skola.png'
import Vez from '../img/cards/building/vez.png'
import Zaklady from '../img/cards/building/zaklady.png'
import Zed from '../img/cards/building/zed.png'

import Ceta from '../img/cards/army/ceta.png'
import Jezdec from '../img/cards/army/jezdec.png'
import Nabor from '../img/cards/army/nabor.png'
import Rytir from '../img/cards/army/rytir.png'
import Saboter from '../img/cards/army/saboter.png'
import Smrtka from '../img/cards/army/smrtka.png'
import Strelec from '../img/cards/army/strelec.png'
import Swat from '../img/cards/army/swat.png'
import Zlodej from '../img/cards/army/zlodej.png'
import Ztec from '../img/cards/army/ztec.png'

import Carodej from '../img/cards/magic/carodej.png'
import CarujCihly from '../img/cards/magic/caruj_cihly.png'
import CarujKrystaly from '../img/cards/magic/caruj_krystaly.png'
import CarujZbrane from '../img/cards/magic/caruj_zbrane.png'
import Drak from '../img/cards/magic/drak.png'
import Kletba from '../img/cards/magic/kletba.png'
import Skritci from '../img/cards/magic/skritci.png'
import ZnicCihly from '../img/cards/magic/znic_cihly.png'
import ZnicKrystaly from '../img/cards/magic/znic_krystaly.png'
import ZnicZbrane from '../img/cards/magic/znic_zbrane.png'

import CardBack from '../img/cards/card_back.png';

const Card = props => {
	var cardImg;

	switch (props.cardType) {
		case "babylon": cardImg = Babylon; break;
		case "hradba": cardImg = Hradba; break;
		case "obrana": cardImg = Obrana; break;
		case "pevnost": cardImg = Pevnost; break;
		case "povoz": cardImg = Povoz; break;
		case "rezervy": cardImg = Rezervy; break;
		case "skola": cardImg = Skola; break;
		case "vez": cardImg = Vez; break;
		case "zaklady": cardImg = Zaklady; break;
		case "zed": cardImg = Zed; break;
		
		case "ceta": cardImg = Ceta; break;
		case "jezdec": cardImg = Jezdec; break;
		case "nabor": cardImg = Nabor; break;
		case "rytir": cardImg = Rytir; break;
		case "saboter": cardImg = Saboter; break;
		case "smrtka": cardImg = Smrtka; break;
		case "strelec": cardImg = Strelec; break;
		case "swat": cardImg = Swat; break;
		case "zlodej": cardImg = Zlodej; break;
		case "ztec": cardImg = Ztec; break;
		
		case "carodej": cardImg = Carodej; break;
		case "caruj_cihly": cardImg = CarujCihly; break;
		case "caruj_krystaly": cardImg = CarujKrystaly; break;
		case "caruj_zbrane": cardImg = CarujZbrane; break;
		case "drak": cardImg = Drak; break;
		case "kletba": cardImg = Kletba; break;
		case "skritci": cardImg = Skritci; break;
		case "znic_cihly": cardImg = ZnicCihly; break;
		case "znic_krystaly": cardImg = ZnicKrystaly; break;
		case "znic_zbrane": cardImg = ZnicZbrane; break;
		
		default:
			return ( <img id={props.id} className="Card" src={CardBack} alt="card_back" /> );
	}
	
	if (props.showCard) {
		return ( <img id={props.id} className="Card PlayableCard" src={cardImg} alt={props.cardType} /> );
	}

	if (props.playable) {
		return (
			<img id={props.id} className="Card PlayableCard" onClick={() => props.playFunction(props.id)} src={cardImg} alt={props.cardType} />
		);
	}
	else {
		return (
			<img id={props.id} className="Card NonPlayableCard" onClick={() => props.discardFunction(props.id)} src={cardImg} alt={props.cardType} />
		);	
	}
}

export default Card;
