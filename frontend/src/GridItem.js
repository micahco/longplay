const GridItem = (props) => {
    const GRID_BASE = 40;

    const itemStyle = {
        width: props.gridSize * GRID_BASE
    }

    const imgStyle = {
        maxWidth: props.gridSize * GRID_BASE,
        maxHeight: props.gridSize * GRID_BASE
    }

    return (
        <div
            className="item" 
            style={itemStyle}
            onClick={props.onClick}
        >
            {props.album.artwork === true ?
            <img
                alt={props.album.name}
                src={`${props.host}/static/img/${props.album.id}.jpg`}
                style={imgStyle}
            /> :
            <div className="missing-art">
                <span>{props.album.artist}</span>
                <span><strong>{props.album.name}</strong></span>
            </div>
            }
        </div>
    )
}

export default GridItem;