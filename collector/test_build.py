"""Offline tests: python3 -m unittest discover -s collector -v"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402
import classify as C  # noqa: E402


class TestRelevance(unittest.TestCase):
    def test_core(self):
        for t in ("A 56 Gb/s 6 mW 300 um2 inverter-based CTLE for short-reach PAM2 applications in 16 nm CMOS",
                  "A 28-Gb/s Single-Ended PAM-4 Receiver With T-Coil-Integrated Continuous-Time Linear Equalizer in 40-nm CMOS Technology",
                  "A 10-Gb/s Inductorless CMOS Analog Equalizer With an Interleaved Active Feedback Topology",
                  "A 1-mW 12-Gb/s continuous-time adaptive passive equalizer in 90-nm CMOS",
                  "A 2.5 Gb/s adaptive cable equalizer",
                  "A 160-MHz analog equalizer for magnetic disk read channels"):
            self.assertEqual(C.relevance(t, ""), "core", t)

    def test_bare_equalizer_needs_an_analog_abstract(self):
        t = "A 10Gb/s CMOS adaptive equalizer for backplane applications"
        self.assertEqual(C.relevance(t, "An equalizer employs reverse scaling and dual-loop adaptation."), "core")
        self.assertIsNone(C.relevance("Low-Power CMOS Equalizer Design for 20-Gb/s Systems",
                                      "This paper describes a half-rate speculative decision-feedback equalizer."))

    def test_receiver_with_a_ctle(self):
        self.assertEqual(C.relevance("A 100Gb/s 1.1pJ/b PAM-4 RX with Dual-Mode Speculative DFE in 14nm CMOS FinFET",
                                     "The receiver comprises a CTLE, a VGA and a 1-tap DFE."), "rx")
        self.assertIsNone(C.relevance("A 100Gb/s PAM-4 RX with Speculative DFE", "The receiver uses a 1-tap DFE."))

    def test_out(self):
        for t in ("A Five-Tap Delay-Line-Based Feed-Forward-Equalizer for 200-Gb/s Wireline Receiver in 28-nm CMOS",
                  "CTLE-Ising: A Continuous-Time Latch-Based Ising Machine Featuring One-Shot Fully Parallel Spin Updates",
                  "A 28-nm dual-port SRAM macro with active bitline equalizing circuitry against write disturb issue",
                  "Low-Overhead Power Side-Channel Resistant AES Accelerator via Activity Equalization",
                  "A 20Gb/s 0.77pJ/b VCSEL transmitter with nonlinear equalization in 32nm SOI CMOS",
                  "Wireline equalization using pulse-width modulation",
                  "A 46 Gbps 12 pJ/b Sparsity-Adaptive Beamspace Equalizer for mmWave Massive MIMO in 22FDX",
                  "Session 21- Adaptive Equalizers for Serial Communications"):
            self.assertFalse(not C.NON_PAPER.search(t) and C.relevance(t, ""), t)


class TestSpecs(unittest.TestCase):
    def test_title(self):
        t = "A 56 Gb/s 6 mW 300 um2 inverter-based CTLE for short-reach PAM2 applications in 16 nm CMOS"
        s = C.parse_specs(t, "")
        self.assertEqual((s["rate"], s["p"], s["node"]), (56e9, 0.006, 16))
        self.assertIn("Inverter-based", C.architectures(t, ""))
        self.assertEqual(C.modulations(t, ""), ["NRZ"])

    def test_boost_and_loss(self):
        s = C.parse_specs("A 25 Gb/s CTLE", "The CTLE provides 15 dB of peaking and compensates 22-dB channel loss.")
        self.assertEqual((s["boost"], s["loss"]), (15.0, 22.0))
        s = C.parse_specs("A CTLE", "Its peaking gain is up to 18 dB at 14 GHz.")
        self.assertEqual(s["boost"], 18.0)
        self.assertNotIn("boost", C.parse_specs("A CTLE", "It equalizes a 20-dB loss channel."))

    def test_several_rates_are_left_out(self):
        self.assertNotIn("rate", C.parse_specs("A CTLE", "It runs at 56 Gb/s in PAM4 and 28 Gb/s in NRZ."))


class TestBuild(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.cache = os.path.join(self.tmp, "cache")
        os.makedirs(self.cache)
        self._papers, self._meta = build.PAPERS, build.META
        build.PAPERS = os.path.join(self.tmp, "papers.json")
        build.META = os.path.join(self.tmp, "meta.json")

    def tearDown(self):
        build.PAPERS, build.META = self._papers, self._meta
        shutil.rmtree(self.tmp)

    def put(self, n, title, pub, abstract="", year=2025):
        with open(os.path.join(self.cache, "%d.json" % n), "w", encoding="utf-8") as f:
            json.dump({"article_number": n, "title": title, "publication_title": pub, "abstract": abstract,
                       "publication_year": year, "publication_date": "Feb. %d" % year, "doi": "10.1109/x.%d" % n,
                       "authors": {"authors": [{"full_name": "A. Kim", "author_order": 1,
                                                "affiliation": "KAIST, Daejeon, South Korea"}]}}, f)

    def test_rebuild(self):
        config = build.load_json(build.CONFIG, None)
        self.put(1, "A 32-Gb/s Adaptive CTLE With Inductive Peaking in 28-nm CMOS", "IEEE Journal of Solid-State Circuits",
                 "It consumes 12 mW.")
        self.put(2, "A 12-b SAR ADC", "IEEE Journal of Solid-State Circuits")
        self.put(3, "A 56-Gb/s PAM-4 Receiver in 7-nm FinFET", "2025 IEEE Custom Integrated Circuits Conference (CICC)",
                 "The receiver has a two-stage CTLE and consumes 150 mW.")
        meta = build.rebuild(config, self.cache, "2026-10-28")
        papers = {p["id"]: p for p in build.load_json(build.PAPERS, [])}
        self.assertEqual(set(papers), {"1", "3"})
        self.assertEqual((papers["1"]["lv"], papers["1"]["s"]["p"], papers["1"]["cal"]), ("core", 0.012, True))
        self.assertIn("Inductive peaking", papers["1"]["ar"])
        self.assertEqual(papers["3"]["lv"], "rx")
        self.assertNotIn("p", papers["3"]["s"])          # the whole receiver's power, not the CTLE's
        self.assertEqual(papers["3"]["s"]["node"], 7)
        self.assertNotIn("abstract", json.dumps(list(papers.values())))
        self.assertEqual((meta["core"], meta["rx"]), (1, 1))


if __name__ == "__main__":
    unittest.main()
