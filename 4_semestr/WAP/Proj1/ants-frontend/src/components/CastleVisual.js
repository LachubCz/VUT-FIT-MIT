import React from 'react'
import CastleBlack from '../img/castle/hrad_cerni_unedited.png'
import CastleRed from '../img/castle/hrad_cerveni_unedited.png'
import FlagBlack from '../img/castle/flag_black.gif'
import FlagRed from '../img/castle/flag_red.gif'
import TrumpetBlack from '../img/castle/trumpet_black.png'
import TrumpetRed from '../img/castle/trumpet_red.png'
import WallImg from '../img/wall/hradba_unedited.BMP'
import GrassTopImg from '../img/castle/grass_top.png'
import GrassBottomImg from '../img/castle/grass_bottom.png'

import CelebrationBlack from '../img/castle/celebration_black.gif'
import CelebrationRed from '../img/castle/celebration_red.gif'

const CastleVisual = props => {
	// determine card img
	var wall_id = "WallRight"
	var castle_id = "CastleRight";
	var grass_class = "GrassRight";

	// compute castle position
	let x = (props.estateStats.castle > 100) ? 100 : props.estateStats.castle;
	let bottom_val = (1.95*x) - 100;
	let clip_path_val = (-0.8*x) + 80;
	let castleStyle = {
		bottom: bottom_val + "px",
		clipPath: "inset(0 0 " + clip_path_val + "% 0)"
	};

	// compute wall position
	let val = (props.estateStats.wall > 100) ? 100 : props.estateStats.wall;
	bottom_val = 1.979798*val - 101.9798;
	clip_path_val = 89.89899 - 0.8989899*val;

	if (val === 0) {
		clip_path_val = 100;
	}

	let wallStyle = {
		bottom: bottom_val + "px",
		clipPath: "inset(0 0 " + clip_path_val + "% 0)"	
	}

	if (props.side === "left") {
		wall_id = "WallLeft";
		castle_id = "CastleLeft"
		grass_class = "GrassLeft"
		return (
			<div className="CastleVisual">
				<div className="CastleDiv" id={castle_id} style={castleStyle} >
					<img className="CastleTrumpet" src={TrumpetBlack} alt="black ant trumpeter"/>
					<img className="CastleFlag" src={FlagBlack} alt="ant castle flag" />
					<img src={CastleBlack} alt="ant castle" />
				</div> 
								
				<img className={"GrassTop " + grass_class} src={GrassTopImg} alt="castle grass" />
				<img className={"GrassBottom " + grass_class} src={GrassBottomImg} alt="castle grass" />

				<img className="Celebration" id="CelebrationLeft" src={CelebrationBlack} alt="black ant celebration" />

				<img className="Wall" id={wall_id} src={WallImg} alt="ant castle wall" style={wallStyle} />
			</div>
		);
	}
	else {
		return (
			<div className="CastleVisual">
				<img className="Wall" id={wall_id} src={WallImg} alt="ant castle wall" style={wallStyle} />

				<div className="CastleDiv" id={castle_id} style={castleStyle}>
					<img className="CastleTrumpet" id="CastleTrumpetRed" src={TrumpetRed} alt="red ant trumpeter"/>
					<img className="CastleFlag" src={FlagRed} alt="ant castle flag" />
					<img className="Castle" id={castle_id} src={CastleRed} alt="ant castle" />
				</div>
				
				<img className={"GrassTop " + grass_class} src={GrassTopImg} alt="castle grass" />
				<img className={"GrassBottom " + grass_class} src={GrassBottomImg} alt="castle grass" />

				<img className="Celebration" id="CelebrationRight" src={CelebrationRed} alt="red ant celebration" />
			</div>
		);
	}
}

export default CastleVisual;


// <img className="Castle" id={castle_id} src={CastleImg} alt="ant castle" />