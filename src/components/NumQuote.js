import React from 'react';
import DisplayQuote from './DisplayQuote.js'
import './Cell.css'
import getTextWidth from '../Functions/TextWidth.js'

//Handles the quote info which is displayed to the user when they choose to add a quote
class NumQuote extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            //number keeps track of the number of the particular layout we are about to add
            //to the quote list
            number: 1
        }
        this.change = this.change.bind(this)
        this.submit = this.submit.bind(this)
    }

    //When they press submit, we call a function in 'App'js' which handles 
    //Adding the quote to the quote list, with the number of this layout
    submit(x) {
        if(x)
            this.props.press(this.state.number)
        else
            this.props.pressDown()
    }

    //When the user changes the number of the layout to be added
    change(x) {
        this.setState({
            number:x
        })
    }
    

    render() {
        if (this.props.mobile) {
            return (<div style={{ alignItems: "center", justifyContent: "center", width: "100%" }}>
                <img src={this.props.clip} className="clipboard" />
                <img src={this.props.cancel} onClick={() => this.submit(false)} className="cancel" />
                <DisplayQuote mobile={true} extraSmall={true} eur={this.props.currency} id={null} popUp={true} currency={this.props.currency} quantity={this.state.number} discount={this.props.discount} total={this.props.total} flashings={this.props.flashings} landscape={this.props.landscape} miniFlashing={this.props.mini} xSize={this.props.xSize} panels={this.props.panels} packers={this.props.packers} width={this.props.xSize} kwp={this.props.kwp} quantityChange={this.change} />
                <img src={this.props.confirm} onClick={() => this.submit(true)} className="confirm" />
            </div>)
        }
        else
            return (<div style={{ alignItems: "center", justifyContent: "center", width: "100%" }}>
                <div style={{ display: "flex", flexDirection:"horizontal" }}>
                    <img src={this.props.clip} className="clipboard" />
                    <input className={"projNamePopup"} value={this.props.projectName} style={{ width: getTextWidth(this.props.projectName, "30px Segoe UI Light") + 16 }} type="text" onChange={this.props.projectNameChange} />
                    <img src={this.props.cancel} onClick={() => this.submit(false)} className="cancel" />
                </div>
                <DisplayQuote quoteNameChange={this.props.quoteNameChange} quoteName={this.props.quoteName} eur={this.props.currency} id={null} popUp={true} currency={this.props.currency} quantity={this.state.number} discount={this.props.discount} total={this.props.total} flashings={this.props.flashings} landscape={this.props.landscape} miniFlashing={this.props.mini} xSize={this.props.xSize} panels={this.props.panels} packers={this.props.packers} width={this.props.xSize} kwp={this.props.kwp} quantityChange={this.change} />
                <img src={this.props.confirm} onClick={() => this.submit(true)} className="confirm" />
            </div>)
    }
}


export default NumQuote;