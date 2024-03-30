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
  const [last_transaction, setLast_transaction] = useState<Transaction | null>(null); // [1


  // Function to fetch the latest transactions and balance based on the client_id
  const fetchLastTransaction  = () => {
    fetch('/api/last_transaction')
      .then((res) => res.json())
      .then((data) => {
        if (!data.client_id) {
          return;
        }
        const last_transaction = {
          date: data.last_transaction.date,
          amount: data.last_transaction.amount,
          type: data.last_transaction.type,
        };
        setLast_transaction(last_transaction);
        setClient_id(data.client_id);
        setBalance(data.balance);
      });
  }

  useEffect(() => {
    fetchLastTransaction();
    // Set up polling every 30 seconds
    const intervalId = setInterval(fetchLastTransaction, 1000);

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
        <p className="z-10 text-2xl font-semibold text-center">You paid</p>
        
        {/* Container for the remaining balance */}
        <div className="z-10 mt-4 flex flex-col items-center justify-center w-full md:w-80 h-20 bg-white shadow-lg rounded-lg">
          <p className="text-lg font-semibold">Remaining balance:{balance}</p>
          {/* get balancefromstate*/}
          <span className="text-xl font-bold">{balance}</span>
        </div>
      </div>

      <div className="mb-32 grid text-center lg:mb-0 lg:grid-cols-2 lg:text-left">

        <a
          href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className={`mb-3 text-2xl font-semibold`}>
            Templates{" "}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
            Explore the Next.js 13 playground.
          </p>
        </a>

        <a
          href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className={`mb-3 text-2xl font-semibold`}>
            Deploy{" "}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
            Instantly deploy your Next.js site to a shareable URL with Vercel.
          </p>
        </a>
      </div>
    </main>
  );
}
