import Image from "next/image";
import Link from "next/link";
"use client"; // This is a client component 👈🏽
import { useState, useEffect } from "react";

interface Transaction {
  date: string;
  amount: number;
  type: string;
}



export default function Home() {
  const [client_id, setClient_id] = useState<string>(""); 
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [balance, setBalance] = useState<number>(0);
  const [last_transaction, setLast_transaction] = useState<Transaction | null>(null);
  const [showTransaction, setShowTransaction] = useState<boolean>(false);


  const onTopUp = () => {
    fetch('/api/topup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ client_id: client_id}),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      });
  }

  const onShowTransaction = () => {
    setShowTransaction(!showTransaction);
  }

  // use effect to fetch transactions history, depend on ahowTransaction
  useEffect(() => {
    if (showTransaction) {
      fetch(`/api/transactions/${client_id}`)
        .then((res) => res.json())
        .then((data) => {      
          setTransactions(data);
                   
        }
      );
    }
    console.log("transactions", transactions);
  }
  , [showTransaction]);
 

  // Function to fetch the latest transactions and balance based on the client_id
  const fetchLastTransaction  = () => {
    fetch('/api/last_transaction')
      .then((res) => res.json())
      .then((data) => {
        if (!data.client_id) {
          return;
        }
        const last_transaction = {
          date: data.transaction.date,
          amount: data.transaction.amount,
          type: data.transaction.type,
        };
        setLast_transaction(last_transaction);
        setClient_id(data.client_id);
        setBalance(data.balance);
      });
  }

  useEffect(() => {
    fetchLastTransaction();
    // Set up polling every 3 seconds
    const intervalId = setInterval(fetchLastTransaction, 3000);

    // Clear interval on component unmount
    return () => clearInterval(intervalId);
  }, [client_id]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none">

        </div>
      </div>
      
      <div className="relative flex flex-col items-center justify-center p-4 before:absolute before:inset-0 before:-z-10 before:rounded-lg before:bg-gradient-to-br before:from-transparent before:via-transparent before:to-blue-500 before:blur-2xl after:absolute after:inset-0 after:-z-20 after:rounded-lg after:bg-gradient-to-br after:from-blue-200 after:to-blue-700 after:blur-3xl">
        {/* Message about the payment */}
        <p className="z-10 text-2xl font-semibold text-center black">{
          last_transaction?.type === "credit"
            ? `You paid ${last_transaction?.amount} on ${last_transaction?.date}`
            : `You top up ${last_transaction?.amount} on ${last_transaction?.date}`
        }</p>
        {/* Container for the remaining balance */}
        <div className="z-10 mt-4 flex flex-col items-center justify-center w-full md:w-80 h-20 bg-black shadow-lg rounded-lg">
          <p className="text-sm font-semibold">Remaining balance:</p>
          {/* get balancefromstate*/}
          <span className="text-xl font-bold">{balance}</span>
        </div>
      </div>

      <div className="mb-32 grid text-center lg:mb-0 lg:grid-cols-2 lg:text-left"
      >

        <div
          className="group text-center rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          onClick={onTopUp}
          cursor-pointer
        >
          <h2 className={`mb-3 text-2xl font-semibold`}>
            Top up
          </h2>
          <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
            Explore the Next.js 13 playground.
          </p>
        </div>

        <div
          className="group text-center rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          onClick={onShowTransaction}
          cursor-pointer
        >
          <h2 className={`mb-3 text-2xl font-semibold`}>
            {showTransaction ? "Hide" : "Show"} Transactions
          </h2>
          <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
            Instantly deploy your Next.js site to a shareable URL with Vercel.
          </p>
        </div>
        <div className="flex-col col-span-2 items-center justify-center ">
          { showTransaction && transactions.length > 0 ? transactions.map((transaction, index) => (
            <div key={index} className="flex mb-10 bg-gray items-center justify-between w-full p-4 shadow-lg rounded-lg  border-gray-300">
              <div>
                <p className="text-sm font-semibold">{transaction.date}</p>
                <p className="text-sm">{transaction.type}</p>
              </div>
              <p className="text-sm font-semibold">{transaction.amount}</p>
              </div>
          ))
          : null} 
        </div>
      </div>
    </main>
  );
}
