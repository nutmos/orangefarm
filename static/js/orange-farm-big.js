var OrangeFarmBig = React.createClass ({
    render: function() {
        var imgStyle = {
            height: '100px',
            marginTop: '3em'
        };
        return (
        <div className="row text-centered">
        <a href="/">
            <img style={imgStyle} src={data.logo} />
        </a>
        </div>);
    }
});

ReactDOM.render(
    React.createElement(OrangeFarmBig, {}),
    document.getElementById('orange-farm-big')
);
