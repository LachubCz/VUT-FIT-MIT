import React from 'react'
import ResourceTile from './ResourceTile'


const PlayerStats = props => {
	return (
		<div className="PlayerStatus">
			<div className="PlayerName">{props.name}</div>

			<ResourceTile type="BuildingStats" workers={props.stats.building.workers} amount={props.stats.building.material}/>
			<ResourceTile type="ArmyStats" workers={props.stats.army.workers} amount={props.stats.army.material}/>
			<ResourceTile type="MagicStats" workers={props.stats.magic.workers} amount={props.stats.magic.material}/>

			<ResourceTile type="CastleStats" workers={props.stats.estate.castle} amount={props.stats.estate.wall}/>
		</div>
	);
}

export default PlayerStats;