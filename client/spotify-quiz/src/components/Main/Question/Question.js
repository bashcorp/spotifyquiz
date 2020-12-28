import React from "react";
import Glide from "@glidejs/glide";

const Question = ({ plan, handleOffer }) => {
  return (
    <div>
      <div onClick={() => handleOffer(plan.id)} className="question-wrapper">
        <div className="question-card">
        <p>
          <h3> Question: {plan.id} </h3>
          <span>id: {plan.price}</span>
          <div>price: {plan.price}</div>
          <div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div><div>price: {plan.price}</div>
        </p>
        </div>
      </div>
    </div>
  );
};

export default Question;
