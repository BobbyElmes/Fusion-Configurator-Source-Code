import React from 'react';
import './Fonts.css';
import '../App.css';

class RollUp extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            optionId: 0
        }
        this.handleChange = this.handleChange.bind(this)
    }

    handleChange(e) {
        if (e.target.value != this.state.optionId) {
            this.props.rollUpChange()
            this.setState({
                optionId: e.target.value
            })
        }
    }

    render() {
        var options = []
        for (var i = 0; i < this.props.options.length; i++)
            options.push(<option value={i}>{this.props.options[i]}</option>)

        if (this.props.mobile)
            return (
                <div class="RollUpContainerMobile">
                    <p class="RollUpMobile Segoe">{this.props.rollUpWord}</p>
                    <select class="RollUpOptionsMobile Arial" value={this.state.optionId} onChange={this.handleChange} >
                        {options}
                    </select>
                </div>)
        else
            return (
                <div class="RollUpContainer">
                    <p class="RollUp">{this.props.rollUpWord}</p>
                    <select class="RollUpOptions" value={this.state.optionId} onChange={this.handleChange} >
                        {options}
                    </select>
                </div>)
    }
}


export default RollUp;