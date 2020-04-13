import React from 'react'
import BuildingWorker from '../img/stats_ui/building_worker.png'
import BuildingMaterial from '../img/stats_ui/building_material.png'
import ArmyWorker from '../img/stats_ui/army_worker.png'
import ArmyMaterial from '../img/stats_ui/army_material.png'
import MagicWorker from '../img/stats_ui/magic_worker.png'
import MagicMaterial from '../img/stats_ui/magic_material_small.png'
import CastleHeight from '../img/stats_ui/castle_height.png'
import WallHeight from '../img/stats_ui/wall_height.png'
/*
function ResourceStatusTile(props) {
	return <div className="ResourceStatusTile">{props.workers}, {props.amount}</div>;
}*/


const ResourceTile = props =>  {
	var worker_img;
	var material_img;
	var worker_desc = "";
	var material_desc = "";
	// determine worker img
	// determine material img

	switch (props.type) {
		case "BuildingStats":
			worker_img = BuildingWorker;
			material_img = BuildingMaterial;
			worker_desc = "Stavitelé";
			material_desc = "Cihly";
			break;
		case "ArmyStats":
			worker_img = ArmyWorker;
			material_img = ArmyMaterial;
			worker_desc = "Vojáci";
			material_desc = "Zbraně";
			break;
		case "MagicStats":
			worker_img = MagicWorker;
			material_img = MagicMaterial;
			worker_desc = "Mágové";
			material_desc = "Krystaly";
			break;
		case "CastleStats":
			worker_img = CastleHeight;
			material_img = WallHeight;
			worker_desc = "Hrad";
			material_desc = "Hradba";
			break;
		default:
			worker_desc = "ERROR";
			material_desc = "ERROR";
			break;
	}
	

	return (
		<div className={"ResourceTile " + props.type} >
			<div className="ResourceTileLine ResourceTileLineFirst">
				<div className="TileLineDesc">
					<img className="PlayerStatImg" src={worker_img} alt="worker icon based on resource type" />
					{worker_desc}
				</div>

				<div className="TileLineValue">{props.workers}</div>
			</div>
			
			<div className="ResourceTileLine">
				<div className="TileLineDesc">
					<img className="PlayerStatImg" src={material_img} alt="material icon based on resource type" />
					{material_desc}
				</div>
				
				<div className="TileLineValue">{props.amount}</div>
			</div>
		</div>
	);
}


export default ResourceTile;